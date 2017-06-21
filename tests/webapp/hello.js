var app = angular.module('myApp', []);
app.controller('myCtrl', function( $scope, $http, $interval ) {
		
	console.log("starting"); 
	$scope.taskid = "";
	$scope.routerConfig ="";
	var myInterval
	$scope.task_response = "";
  //	$scope.statusReady = false	
  $scope.lsname = "";
  $scope.ls_response = "";
  $scope.lsnameList = "";
  $scope.new_lsname = "";
  $scope.username = "";
  $scope.password = "";
  $scope.new_lsname_response = "";
  $scope.deleted_lsname_response = "";
  $scope.delete_lsname = "";
  $scope.delete_username= "";


$scope.clearAll = function() {
      console.log("Clearing");
      $scope.routerConfig = "";
      $scope.task_response = "";
      $scope.lsname = "";
      $scope.ls_response = "";
      $scope.lsnameList = "";
      $scope.new_lsname = "";
      $scope.username= "";
      $scope.password="";
      $scope.rights="";
      $scope.fullname="";
};

$scope.getTaskStatus = function () {
	//function getTaskStatus(){
		  	//console.log("inside getTaskStatus 1 : " + $scope.statusReady); 
	       	$http.get($scope.uriStatus).        	
        	success(function(data) {
				$scope.statusReady = data;       			
       			console.log("inside getTaskStatus : "+$scope.statusReady);	
       			}, function(error) {

        		console.error("no data retrieved  for routerConfig" + angular.toJson(error, true)); // TODO Remove console logging
        		//$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
        		$scope.routerMX = "no data retrieved ...";
        		//$window.scrollTo(0,0);
        	});
}


$scope.getTaskResponse = function () {
	//function getTaskStatus(){
		  	//console.log("inside getTaskStatus 1 : " + $scope.statusReady); 
	       	$http.get($scope.uriValue).        	
        	success(function(data) {
				$scope.task_response = data;       			
       			console.log("inside task_response : "+$scope.task_response);	
       			}, function(error) {

        		console.error("no data retrieved  for task_response" + angular.toJson(error, true)); // TODO Remove console logging
        		//$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
        		$scope.routerMX = "no data retrieved ...";
        		//$window.scrollTo(0,0);
        	});
}


$scope.getConfigTaskid = function () {
	console.log("starting"); 

	$http.get('http://147.102.22.76:8000/physicalsys_async/').
      success(function(data) {
		    var id = data.slice(1,data.length-1);
       	$scope.taskid = id;
       	console.log("@@@taskid "+id );	
        $scope.uriStatus = 'http://147.102.22.76:8000/task_status/'+encodeURIComponent(id)+'/'
        $scope.uriValue = 'http://147.102.22.76:8000/task_response/'+encodeURIComponent(id)+'/'
    	  console.log("@@@customURI :"+ $scope.uriStatus);	
    
		    var i = 0;
		
		    promise = $interval( function(){ 
			      $scope.getTaskStatus(); 			
			      date = new Date();
            console.log("time ="+date);
            console.log("inside interval statusReady: " + $scope.statusReady); 
    			  if ($scope.statusReady === "true"){
    				  console.log("inside if: " + $scope.statusReady); 
       			  $scope.stop();
       			  $scope.getTaskResponse(); 
       		   }
		    }, 2000, [20]);

		    console.log("outside interval statusReady: " + $scope.statusReady); 
      }, function(error) {
        console.error("no data retrieved " + angular.toJson(error, true)); // TODO Remove console logging
        //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
        $scope.taskid = "no data retrieved ...";        
      });
};




$scope.stop = function() {
      console.log("stoppppppppp inteval canceled "+$scope.statusReady);
      $interval.cancel(promise);
};
	


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






});