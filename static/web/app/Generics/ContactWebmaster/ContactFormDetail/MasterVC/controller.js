(function () {
  'use strict';
  angular.module('app.FUSE_APP_NAME').controller('FUSE_APP_NAMEController', FUSE_APP_NAMEController);

  function FUSE_APP_NAMEController($log, $state, GenericContactDetail) {
    let vm = this;
    vm.$onInit = onInit;
    vm.$onDestroy = onDestroy;

    vm.viewName = 'FUSE_APP_NAME';
    vm.viewDidLoad = viewDidLoad;

    vm.loadData = loadData;
    vm.deleteThis = deleteThis;
    vm.notFound404 = notFound404;



    vm.contactFormId = -1;

    vm.viewData = {};


    function onInit() {
      vm.viewDidLoad();
    }

    function onDestroy() {

    }

    function viewDidLoad() {
      $log.log('FUSE_APP_NAME did finish loading');
      if ($state.params.contactFormId) {
        vm.contactFormId = $state.params.contactFormId;
        vm.loadData();
      } else {
        vm.notFound404();
      }
    }

    function loadData() {
      GenericContactDetail.getById(vm.contactFormId)
        .then(function(responseData) {
        vm.viewData = responseData;
      });
    }

    function deleteThis() {
      GenericContactDetail.deleteById(vm.contactFormId)
        .then(function(responseData) {
        if (responseData.result === "SUCCESS") {
          vm.infoBox = "This message has been archived, it won't be displayed in the list anymore.";
        } else {
          vm.infoBox = "Something bad happened, failed to archive this message.";
        }
      });
    }

    function notFound404() {
      vm.notFound = "404 NOT FOUND";
    }
  }
})();