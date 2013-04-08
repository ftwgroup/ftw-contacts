function forEach(obj, iterator, context) {
  var key;
  if (obj) {
    if (isFunction(obj)){
      for (key in obj) {
        if (key != 'prototype' && key != 'length' && key != 'name' && obj.hasOwnProperty(key)) {
          iterator.call(context, obj[key], key);
        }
      }
    } else if (obj.forEach && obj.forEach !== forEach) {
      obj.forEach(iterator, context);
    } else if (isArrayLike(obj)) {
      for (key = 0; key < obj.length; key++)
        iterator.call(context, obj[key], key);
    } else {
      for (key in obj) {
        if (obj.hasOwnProperty(key)) {
          iterator.call(context, obj[key], key);
        }
      }
    }
  }
  return obj;
}

/**
 * throw error of the argument is falsy.
 */
function assertArg(arg, name, reason) {
  if (!arg) {
    throw new Error("Argument '" + (name || '?') + "' is " + (reason || "required"));
  }
  return arg;
}

function assertArgFn(arg, name, acceptArrayAnnotation) {
  if (acceptArrayAnnotation && isArray(arg)) {
      arg = arg[arg.length - 1];
  }

  assertArg(isFunction(arg), name, 'not a function, got ' +
      (arg && typeof arg == 'object' ? arg.constructor.name || 'Object' : typeof arg));
  return arg;
}

// this is for injecting dependencies into functions

var FN_ARGS = /^function\s*[^\(]*\(\s*([^\)]*)\)/m;
var FN_ARG_SPLIT = /,/;
var FN_ARG = /^\s*(_?)(\S+?)\1\s*$/;
var STRIP_COMMENTS = /((\/\/.*$)|(\/\*[\s\S]*?\*\/))/mg;

function annotate(fn) {
  var $inject,
      fnText,
      argDecl,
      last;
  // if we have a function then convert to string and extract arguments    
  if (typeof fn == 'function') {
    if (!($inject = fn.$inject)) {
      $inject = [];
      fnText = fn.toString().replace(STRIP_COMMENTS, '');
      argDecl = fnText.match(FN_ARGS);
      forEach(argDecl[1].split(FN_ARG_SPLIT), function(arg){
        arg.replace(FN_ARG, function(all, underscore, name){
          $inject.push(name);
        });
      });
      fn.$inject = $inject;
    }
  // if we have an array, then assert that the last element is a function
  // and inject the previous elements into the function  
  } else if (isArray(fn)) {
    last = fn.length - 1;
    assertArgFn(fn[last], 'fn')
    $inject = fn.slice(0, last);
  } else {
    assertArgFn(fn, 'fn', true);
  }
  return $inject;
}

// create the injector
function createInjector(modulesToLoad) {
	var INSTANTIATING = {},
		providerSuffix = 'Provider',
		path = [],
		loadedModules = new HashMap(),
		providerCache = {
			$provider: {
				provider: supportObject(provider),
				factory: supportObject(factory),
				service: supportObject(service),
				value: supportObject(value),
				constant: supportObject(constant),
				decorator: supportObject(decorator)
			}
		},
		providerInjector = (providerCache.$injector = 
			createInternalInjector(providerCache, function() {
				throw Error('Unknown provider: ' + path.join(' <- '));
			})),
		instanceCache = {},
		instanceInjector = (instanceCache.$injector = 
			createInternalInjector(instanceCache, function(servicename) {
				var provider = providerInjector.get(servicename + providerSuffix);
				return instanceInjector.invoke(provider.$get, provider);
			}));

	forEach(loadedModules(modulesToLoad), function(fn) { instanceInjector.invoke(fn || noop); });

	return instanceInjector;

	function supportObject(delegate) {
		return function(key, value) {
			if (isObject(key)) {
				forEach(key, reverseParams(delegate));
			} else {
				return delegate(key, value);
			}
		}
	}

	function provider(name, provider_) {
		if (isFunction(provider_) || isArray(provider_)) {
			provider_ = providerInjector.instantiate(provider_);
		}
		if (!provider_.$get) {
			throw new Error('Provider ' + name + ' must define $get factory method.');
		}
		return providerCache[name + providerSuffix] = provider_;
	}

	function factory(name, factoryFn) { return provider(name, { $get: factoryFn }); }

	function service(name, constructor) {
		return factory(name, ['$injector', function($injector) {
			return $injector.instantiate(constructor);
		}]);
	}

	function value(name, value) { return factory(name, valueFn(value)); }

  	function constant(name, value) {
    	providerCache[name] = value;
    	instanceCache[name] = value;
  	}

	function decorator(serviceName, decorFn) {
	    var origProvider = providerInjector.get(serviceName + providerSuffix),
	        orig$get = origProvider.$get;

	    origProvider.$get = function() {
	      		var origInstance = instanceInjector.invoke(orig$get, origProvider);
	      		return instanceInjector.invoke(decorFn, null, {$delegate: origInstance});
	   	};
	}
}
