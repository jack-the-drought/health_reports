(function () {

  'use strict';

  angular.module('myApp', [], function($interpolateProvider) {
      $interpolateProvider.startSymbol('[[');
      $interpolateProvider.endSymbol(']]');
  })

  .controller('myController', ['$scope', '$http',
    function($scope, $http ,$interpolateProvider) {


    $scope.getPopular = function(){
    $http.get("/view1",{
    params: { day: $scope.day }
     })
    .then(function(response) {
      $scope.popular=response.data
     })
    }

    $scope.getTotalDevicesPerDay = function(){
    $http.get("/view2",{
    params: { status: $scope.selectedStatus,type:$scope.selectedType }
     })
    .then(function(response) {
      $scope.totaldevices=response.data
     })
    }

     var getstatusesntypes = function(){
       $http.get("/statusesntypes")
       .then(function(response){
         $scope.statusesntypes = response.data
       })
     }

     getstatusesntypes()


   }

 ]);

}());
