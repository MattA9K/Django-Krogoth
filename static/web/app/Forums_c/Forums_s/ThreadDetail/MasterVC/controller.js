(function() {
    'use strict';
    angular.module('app.FUSE_APP_NAME').controller('FUSE_APP_NAMEController', FUSE_APP_NAMEController);

    function FUSE_APP_NAMEController($state, ThreadDetailREST, $log) {
        var vm = this;
        vm.$onInit = onInit;
        vm.viewName = 'FUSE_APP_NAME';
        vm.viewDidLoad = viewDidLoad;
        vm.loadReplies = loadReplies;
        vm.postReply = postReply;
        vm.loadOP = loadOP;
        vm.backToCategory = backToCategory;
        vm.finalizeReply = finalizeReply;

        vm.opData = {};
        vm.replyInput = "";
        vm.repliesData = {};
        vm.threadId = "";

        function onInit() {
            vm.viewDidLoad();
        }

        function viewDidLoad() {
            console.log('FUSE_APP_NAME did finish loading');
            /// vm.viewName = $state.params.threadId;
            vm.threadId = $state.params.threadId;

            vm.loadOP();
        }

        function loadOP() {
            ThreadDetailREST.getThreadOP(vm.threadId)
                .then(function(opData) {
                    vm.opData = opData;
                    $log.debug(opData);
                    vm.loadReplies(vm.threadId);
                });
        }

        function loadReplies(id) {
            //if (vm.threadId === "") {
            //    $state.go("app.Forums");
            //}
            ThreadDetailREST.getRepliesToThread(id).then(function(data) {
                vm.repliesData = data;
            });
        }

        function postReply() {
            $log.log("POSTing new reply now...");
            ThreadDetailREST.postReply(vm.replyInput, vm.threadId).then(function(response) {
                $log.log("New reply created successfully");
                console.log(response);
                vm.repliesData.results.push(response);
                vm.replyInput = "";
                // vm.finalizeReply();
            });

        }

        function finalizeReply() {
            $log.log("FINALIZING REPLY");
            //ThreadDetailREST.updateParent(vm.threadId).then(function(response) {
            //    $log.info(response);
            //    $log.log("Reply finalization complete!!");
            //});
        }

        function backToCategory() {
            $state.go("app.ForumCategory", {
                "catId": vm.opData.category
            });
        }
    }
})();