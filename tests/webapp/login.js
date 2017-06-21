var app = angular.module('myApp', []);
app.controller('loginCtrl', function( $scope, $http, $window  ) {
		
	
  $scope.username = "";
  $scope.password = "";
  $scope.login_response = "";

$scope.clear = function() {
      console.log("Clearing");
      $scope.username= "";
      $scope.password="";
};



$scope.doLogin = function() {
      
      console.log("username: "+$scope.username);
      console.log("pass: "+$scope.password);
     
      $scope.postObject = {
          username: $scope.username,
          password: $scope.password
      }

      $scope.loginURI = 'http://147.102.22.76:8000/signin/'
      
      $http.post($scope.loginURI,$scope.postObject).         
          success(function(data) {
            $scope.login_response = data;
            console.log("inside login_response : "+$scope.login_response);  
            $window.location.href = '/'
            $location.path('/147.102.22.76:8000/');
            //$location.path(/);
            }, function(error) {
            $scope.login_response = error;
            console.error("no data retrieved  for login_response" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."            
          });
}


/*
$scope.getLSConfig = function() {
      console.log("retrieving configuration for LS "+$scope.lsname);
      $scope.lsconfigURI = 'http://147.102.22.76:8000/logicalsys/'+$scope.lsname+'/'
      
      $http.get($scope.lsconfigURI).         
          success(function(data) {
        $scope.ls_response = data;            
            console.log("inside ls_response : "+$scope.ls_response);  
            }, function(error) {

            console.error("no data retrieved  for ls_response" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.ls_response = "no data retrieved ...";
            //$window.scrollTo(0,0);
          });
}

$scope.getLS = function() {
      console.log("retrieving LS names ");
      $scope.lsListURI = 'http://147.102.22.76:8000/logicalsys/'
      
      $http.get($scope.lsListURI).         
          success(function(data) {
        $scope.lsnameList = data;            
            console.log("inside ls list : "+$scope.lsnameList);  
            }, function(error) {

            console.error("no data retrieved  for ls list" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.lsnameList = "no data retrieved ...";
            //$window.scrollTo(0,0);
          });
};


$scope.createLS = function() {

        $scope.postObject = {
          lsname: $scope.new_lsname,
          username: $scope.username,
          password: $scope.password,
          rights: $scope.rights,
          fullname: $scope.fullname
        }
      
      console.log("create new LS postObject:" + angular.toJson($scope.postObject, true)); // TODO Remove console logging
      var lspostURI = 'http://147.102.22.76:8000/logicalsys/'
      //$http.post('/someUrl', data, config).then(successCallback, errorCallback);
      $http.post(lspostURI,$scope.postObject).         
          success(function(data) {
        $scope.new_lsname_response = data;            
            console.log("inside new_lsname_response : "+$scope.new_lsname_response);  
            }, function(error) {

            console.error("no data retrieved  for new_lsname_response" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.new_lsname_response = "no data retrieved ...";
            //$window.scrollTo(0,0);
          });
}

*/
});