
angular.module('jqueryUI', []).
    directive('autoComplete', function($timeout) {
        var tags = ['donor', 'volunteer', 'student'];
        function split(val) {
            return val.split(/,\s*/);
        }
        function extractLast(term) {
            return split(term).pop();
        }
        return function(scope, iElement, attrs) {
            iElement.autocomplete({
                minLength: 0,
                source: function(request, response) {
                    response($.ui.autocomplete.filter(
                        tags, extractLast(request.term)
                    ));
                }, //'/api/tags',
                focus: function() {
                    return false;
                },
                select: function(event, ui) {
                    // logic for multiple select jqueryUI autoComplete
                    var terms = split(this.value);
                    // remove the current input
                    terms.pop();
                    // add the selected item
                    terms.push(ui.item.value);
                    // add placeholder to get the comma-and space at the end
                    terms.push("");
                    this.value = terms.join(", ");
//                    scope.$digest(); // add this to update services watching this model
                    return false;
                }
            });
        }
    });

angular.module('contacts', ['contactServices', 'jqueryUI']).
    config(['$routeProvider', function($routeProvider) {
        $routeProvider.
            when('/contacts', {templateUrl: '/partials/contacts-list/',
                         controller: ContactListCtrl}).
            when('/contacts/:contactId', {templateUrl: '/partials/contacts-detail/',
                         controller: ContactDetailCtrl})
            .when('/contacts/upload', {templateUrl: '/partials/contacts-upload/', controller: ContactUploadCtrl})
            .otherwise({redirectTo: '/contacts'});
    }]).
    config(['$httpProvider', function($httpProvider) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = csrftoken;
    }]);
