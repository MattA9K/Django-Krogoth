(function() {
    'use strict';
    angular.module('app.FUSE_APP_NAME').controller('FUSE_APP_NAMEController', FUSE_APP_NAMEController);

    function FUSE_APP_NAMEController(ForumNewThread, $state, $mdToast, $log, $timeout) {
        var vm = this;
        vm.$onInit = onInit;
        vm.viewName = 'FUSE_APP_NAME';
        vm.viewDidLoad = viewDidLoad;


        vm.didPressNewThread = didPressNewThread;
        vm.category = "";

        vm.errorToast = errorToast;

        function onInit() {
            vm.viewDidLoad();
        }

        function viewDidLoad() {
            console.log('FUSE_APP_NAME did finish loading');
            vm.category = $state.params.catId;
        }

        function didPressNewThread() {
            //vm.threadInput
            //vm.threadTitle
            if (vm.threadTitle === "" || vm.threadInput === "") {
                vm.errorToast();
            } else {
                ForumNewThread.submitNewThread(vm.category, vm.threadTitle, vm.threadInput)
                    .then(function(newThreadData) {

                        $log.debug("SERVER RETURNED THIS RESPONSE: ");
                        $log.info(newThreadData);

                        $timeout(function() {
                            $state.go("app.ThreadDetail", {
                                "threadId": newThreadData.uid
                            });
                        }, 500);
                    });
            }
        }


        function errorToast() {
            $mdToast.show(
                $mdToast.simple()
                .textContent("You can't submit a thread with a blank title or body.")
                .position("bottom left")
                .hideDelay(3000)
            );
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