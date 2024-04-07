(function() {
    'use strict';
    angular.module('app.FUSE_APP_NAME').controller('FUSE_APP_NAMEController', FUSE_APP_NAMEController);

    function FUSE_APP_NAMEController($state, ForumThreadsREST) {
        var vm = this;

        vm.$onInit = onInit;
        vm.viewName = 'FUSE_APP_NAME';
        vm.viewDidLoad = viewDidLoad;

        vm.loadThreadData = loadThreadData;
        vm.openThread = openThread;
        vm.category = "";
        vm.didPressNewThread = didPressNewThread;
        vm.threadsData = {};

        vm.arrayThreads = [];


        function onInit() {
            vm.viewDidLoad();
        }

        function viewDidLoad() {
            console.log('FUSE_APP_NAME did finish loading');
            // vm.viewName = $state.params.catId;
            vm.loadThreadData();
        }

        function loadThreadData() {
            vm.category = $state.params.catId;
            ForumThreadsREST.getThreads(vm.category).then(function(data) {
                vm.threadsData = data;
                vm.arrayThreads = data.results
            });
        }

        function openThread(id) {
            $state.go("app.ThreadDetail", {
                "threadId": id
            });
        }

        function didPressNewThread() {
            $state.go("app.NewThread", {
                "catId": vm.category
            });
        }
    }
})();





/*
sh /Vol
*/

/*
sh /Volumes/MBP_Backup/arm-prime/docker/KILL_ALL_.sh
*/

/*
sh /Volumes/MBP_Backup/arm-prime/docker/run-docker-installed.sh
*/