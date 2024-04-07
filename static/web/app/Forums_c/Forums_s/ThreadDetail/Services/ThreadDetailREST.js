(function() {
    'use strict';
    angular
        .module('app.FUSE_APP_NAME')
        .factory('_DJANGULAR_SERVICE_NAME_', _DJANGULAR_SERVICE_NAME_);

    /** @ngInject */
    function _DJANGULAR_SERVICE_NAME_($log, $http, $q, $cookies) {
        $log.log('Hello. The service _DJANGULAR_SERVICE_NAME_ is online ! ! !');
        var service = {
            getRepliesToThread: getRepliesToThread,
            postReply: postReply,
            getThreadOP: getThreadOP,
            updateParent: updateParent
        };

        function getThreadOP(id) {
            $log.info('/krogoth_social/api/ForumThreadOP/' + id + '/?format=json');
            var deferred = $q.defer();
            $http({
                method: 'GET',
                url: '/krogoth_social/api/ForumThreadOP/' + id + '/?format=json'
            }).then(function successCallback(response) {
                /// Success  
                deferred.resolve(response.data);
            }, function errorCallback(response) {
                /// Fail
                deferred.reject(response);
            });
            return deferred.promise;
        }

        function getRepliesToThread(id) {
            var deferred = $q.defer();
            $http({
                method: 'GET',
                url: '/krogoth_social/api/ForumThreadReply/?format=json&parent=' + id
            }).then(function successCallback(response) {
                /// Success
                deferred.resolve(response.data);
            }, function errorCallback(response) {
                /// Fail
                deferred.reject(response);
            });
            return deferred.promise;
        }

        function postReply(text, parent) {
            var wrapper = {
                "parent": parent,
                "content": text
            };
            $log.info("POSTING REPLY: ");
            $log.log(wrapper);
            var deferred = $q.defer();
            $http({
                method: 'POST',
                data: wrapper,
                url: '/krogoth_social/api/ForumThreadReply/'
            }).then(function successCallback(response) {
                /// Success
                deferred.resolve(response.data);
            }, function errorCallback(response) {
                /// Fail
                deferred.reject(response);
            });
            return deferred.promise;
        }

        function updateParent(parent) {
            /*
            var deferred = $q.defer();
            $http({
                method: 'GET',
                url: '/krogoth_social/update_thread_moddate/?threadId=' + parent
            }).then(function successCallback(response) {
                /// Success
                deferred.resolve(response.data);
            }, function errorCallback(response) {
                /// Fail
                deferred.reject(response);
            });
            return deferred.promise;
			*/
        }

        return service;
    }
})();