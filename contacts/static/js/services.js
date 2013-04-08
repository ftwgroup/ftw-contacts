
angular.module('contactServices', ['ngResource']).
    factory('Contact', function($resource) {
        return $resource('/api/contacts/:contactId', {contactId: '@id'}, {
            query: {method: 'GET', params:{contactId:''}, isArray:true}
        });
    })
    .factory('Tag', function($resource) {
        return $resource('/api/tags/:tagId', {tagId: '@id'}, {
            query: {method: 'GET', params:{tagId:''}, isArray:true}
        });
    });

