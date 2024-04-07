(function() {
    'use strict';
    angular
        .module('app.FUSE_APP_NAME')
        .factory('_DJANGULAR_SERVICE_NAME_', _DJANGULAR_SERVICE_NAME_);

    /** @ngInject */
    function _DJANGULAR_SERVICE_NAME_($log, $http, $q) {
        $log.log('Hello. The service _DJANGULAR_SERVICE_NAME_ is online ! ! !');
        var service = {
            getCategories: getCategories
        };


        function getCategories() {
            var deferred = $q.defer();
            $http({
                method: 'GET',
                url: '/krogoth_social/api/ForumThreadCategory/'
            }).then(function successCallback(response) {
                /// Success
                deferred.resolve(response.data);
            }, function errorCallback(response) {
                /// Fail
                deferred.reject(response);
            });
            return deferred.promise;
        }



        /*
        function createNew(treeRoot, newName) {
            var payload = {};
            payload["title"] = newName + "_Untitled";
            payload["name"] = newName + "_" + makeid();
            $log.info("  🎲  RANDOM STRING GENERATED  🎲  ");
            $log.log(payload["name"]);
            const RESTfulURI = '/krogoth_gantry/viewsets/' + treeRoot.class + '/';
            var deferred = $q.defer();
            $http({
                method: 'POST',
                data: payload,
                url: RESTfulURI
            }).then(function successCallback(response) {
                /// Success
                deferred.resolve(response.data);
            }, function errorCallback(response) {
                /// Fail
                deferred.reject(response);
            });
            return deferred.promise;
        }
		*/


        return service;
    }
})();