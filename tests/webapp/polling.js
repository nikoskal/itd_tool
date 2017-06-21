app.controller('myCtrl2', function( $scope, $http, $interval ) {
		
	console.log("starting"); 
	$scope.taskid = "";
	$scope.routerConfig ="";
	var myInterval
	$scope.task_response = "";
//	$scope.statusReady = false	
	date = new Date();
    console.log("start time ="+date);



	$scope.GetMX = function () {
		console.log("starting"); 

		$http.get('http://147.102.22.76:8000/routersMX/').
      	success(function(data) {
			console.log("@@@data "+data );	    
       		$scope.routerConfig = data;
        	date2 = new Date();
        	console.log("stop time ="+date2);
       }, function(error) {
        console.error("no data retrieved " + angular.toJson(error, true)); // TODO Remove console logging
        //$scope.warningMessage = "Devices could not be added. Please, check the parameters of the new devices and try again."
        $scope.taskid = "no data retrieved ...";        
       });
	};

});