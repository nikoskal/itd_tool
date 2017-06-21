var app = angular.module('myApp', []);
app.controller('accountCtrl', function( $scope, $http, $interval ) {
		
	console.log("starting"); 
	
  $scope.email = "";
  $scope.username = "";
  $scope.password = "";
  $scope.fullname = "";
  $scope.academic = "";

  $scope.accountObject = "";
  $scope.user_response = "";

  $scope.user_List = "";

$scope.clearAll = function() {
  console.log("Clearing");
  $scope.email = "";
  $scope.username = "";
  $scope.password = "";
  $scope.fullname = "";
  $scope.academic = "";
  $scope.user_postObject = "";
  $scope.user_response = "";
};



$scope.getAccountDetails = function() {
      console.log("retrieving configuration for LS "+$scope.username);
      $scope.accountURI = 'http://147.102.22.76:8000/users/'+$scope.username+'/'
      
      $http.get($scope.accountURI).         
          success(function(data) {
        $scope.user_response = data;            
            console.log("inside user_response : "+$scope.user_response);  
            }, function(error) {
            console.error("no data retrieved for user" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.user_response = "no data retrieved ...";
            //$window.scrollTo(0,0);
          });
}


$scope.getAllUsersLS = function() {
      console.log("retrieving users ");
      $scope.userListURI = 'http://147.102.22.76:8000/users/'
      
      $http.get($scope.userListURI).         
          success(function(data) {
        $scope.user_List = data;            
            console.log("inside user list : "+$scope.user_List);  
            }, function(error) {
            console.error("no data retrieved  for ls list" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.lsnameList = "no data retrieved ...";
            //$window.scrollTo(0,0);
          });
};


$scope.createUser = function() {

      $scope.user_postObject = {
          email: $scope.email,
          username: $scope.username,
          password: $scope.password,
          fullname: $scope.fullname,
          academic: $scope.academic
      }
      
      console.log("create new user:" + angular.toJson($scope.user_postObject, true)); // TODO Remove console logging
      var userpostURI = 'http://147.102.22.76:8000/users/'
      //$http.post('/someUrl', data, config).then(successCallback, errorCallback);
      $http.post(userpostURI,$scope.user_postObject).         
          success(function(data) {
        $scope.new_user_response = data;            
            console.log("inside new_user_response : "+$scope.new_user_response);  
            }, function(error) {
            console.error("no data retrieved for new_user_response" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.new_user_response = "no data retrieved ...";
            //$window.scrollTo(0,0);
          });
}

/*
$scope.deleteLS = function() {

        $scope.deleteObject = {
          lsname: $scope.delete_lsname,
          username: $scope.delete_username
        }
      
      console.log("delete existing LS deleteObject:" + angular.toJson($scope.deleteObject, true)); // TODO Remove console logging
      var lsDeleteURI = 'http://147.102.22.76:8000/logicalsys/'+$scope.delete_lsname+'/'
      console.log("delete existing LS uri:" + lsDeleteURI); 
      //$http.post('/someUrl', data, config).then(successCallback, errorCallback);
      

      //$http.delete('/roles/' + roleid, {request: {username: $scope.delete_username}}).then..
      //$http.delete(lsDeleteURI, $scope.deleteObject).         
      $http.delete(lsDeleteURI, {request: {'username': $scope.delete_username}} ).         
          success(function(data) {
        $scope.deleted_lsname_response = data;            
            console.log("inside deleted_lsname_response : "+$scope.deleted_lsname_response);  
            }, function(error) {

            console.error("no data retrieved  for deleted_lsname_response" + angular.toJson(error, true)); // TODO Remove console logging
            //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
            $scope.deleted_lsname_response = "no LS deleted ...";
            //$window.scrollTo(0,0);
          });
}
*/
});