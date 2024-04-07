(function() {
    'use strict';
    angular.module('app.FUSE_APP_NAME').controller('FUSE_APP_NAMEController', FUSE_APP_NAMEController);

    function FUSE_APP_NAMEController(ForumCategoryREST, $state) {
        var vm = this;
        vm.$onInit = onInit;
        vm.viewName = 'FUSE_APP_NAME';
        vm.viewDidLoad = viewDidLoad;


        vm.loadCategories = loadCategories;
        vm.didPressCategory = didPressCategory;
        vm.categoriesData = {};


        function onInit() {
            vm.viewDidLoad();
        }

        function loadCategories() {
            ForumCategoryREST.getCategories().then(function(data) {
                vm.categoriesData = data;
            });
        }

        function viewDidLoad() {
            console.log('FUSE_APP_NAME did finish loading');
            vm.loadCategories();
        }


        function didPressCategory(uid) {
            $state.go('app.ForumCategory', {
                'catId': uid
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