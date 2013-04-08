function ContactListCtrl($scope, $http, Contact, Tag) {
    $scope.contacts = Contact.query();
    $scope.tags = Tag.query();
    $scope.showAddForm = false;
    $scope.showUploadForm = false;

    $scope.showAddContact = function() {
        $scope.showAddForm = !$scope.showAddForm;
        if ($scope.showAddForm)
            $scope.showUploadForm = false;
    };

    $scope.showUploadContact = function() {
        $scope.showUploadForm = !$scope.showUploadForm;
        if ($scope.showUploadForm)
            $scope.showAddForm = false;
    };

    $scope.addContact = function(newContact) {
//        newContact.account = account_id;
        var contact = new Contact(newContact);
        contact.$save({}, function(response) {
            // success callback
            console.log(response);
            $scope.contacts.push(response);
            // TODO replace this for loop with something more efficient
            for (var prop in newContact) {
                newContact[prop] = '';
            }
            alert('successfully added NEW contact');
        }, function(response) {
            // error callback
            console.log(response);
            data = response.data;
            var errors = '';
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    if (data[key] instanceof Array) {                        
                        for (var i = 0; i < data[key].length ; i++) {
                            errors += key + ': ' + data[key][i] + "\n";
                        }
                    }
                }
            }
            alert(errors);
        });
    };

    $scope.editContact = function(contact) {
        alert("alerts work in angular!");
    }

    // TODO
    $scope.addContactTags = function(contact) {
        alert("TODO");
    }

    $scope.deleteContact = function(contact) {
        contact.$delete();
        console.log($scope.contacts);

        // why doesnt this happen automatically???
        $scope.contacts = $scope.contacts.filter(function (element, index, array) {
            console.log(element);
            return (element.id != contact.id);
        });
    }

    $scope.reset = function(field, index) {
        console.log('field', field);
        console.log('index', index);
        return field = '';
    }
}

function ContactDetailCtrl($scope, $routeParams, Contact, Tag) {
    $scope.contact = Contact.get({contactId: $routeParams.contactId});
    $scope.contactId = $routeParams.contactId;
}

function ContactUploadCtrl($scope, $routeParams, Contact, Tag) {
}

function TagListCtrl($scope) {
    $scope.tags = ['hello', 'foo', 'bar', 'world'];
}
