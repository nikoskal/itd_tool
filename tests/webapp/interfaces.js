var app = angular.module('myApp', []);
app.controller('myCtrl2', function( $scope, $http, $interval ) {
		
	console.log("starting"); 
	$scope.lsname = "";
  $scope.ls_ifcs_response = "";
  $scope.ifcname = "";
  $scope.ifcname_response = "";
  $scope.ifclsname = "";

  $scope.clearAll = function() {
      console.log("Clearing");
  };


  $scope.getInterfacesList = function () {
	   
    console.log("inside getInterfacesList lsname: " + $scope.lsname);  
    console.log("inside getInterfacesList lsname: " + $scope.lsname);  
    $scope.ifcsListURI = 'http://147.102.22.76:8000/logicalsys/'+$scope.lsname+'/ifcs'

    $http.get($scope.ifcsListURI).        	
     	success(function(data) {
		  $scope.ls_ifcs_response = data;       			
     	//console.log("inside getTaskStatus : "+$scope.statusReady);	
    	  }, function(error) {
      	console.error("no interfaces retrieved " + angular.toJson(error, true)); // TODO Remove console logging
    		$scope.ls_ifcs_response = "no interfaces data retrieved ...";
    });

  }


$scope.getInterfaceDetails = function () {
     
    console.log("inside getInterfaceDetails lsname: " + $scope.lsname);  
    console.log("inside getInterfaceDetails ifcname: " + $scope.ifcname);  
    $scope.ifcURI = 'http://147.102.22.76:8000/logicalsys/'+$scope.ifclsname+'/ifcs/'+$scope.ifcname

    $http.get($scope.ifcURI).          
      success(function(data) {
      $scope.ifcname_response = data;             
      //console.log("inside getTaskStatus : "+$scope.statusReady);  
        }, function(error) {
        console.error("no interfaces retrieved " + angular.toJson(error, true)); // TODO Remove console logging
        $scope.ifcname_response = "no interface details retrieved ...";
    });

  }






});