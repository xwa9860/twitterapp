(function () {
  'use strict';

  angular.module('TwitterApp', [])
  .controller('TwitterAppController', ['$scope', '$log', '$http', '$timeout',
    function($scope, $log, $http, $timeout) {

    $scope.getResults = function() {

      $log.log("test");

      // get the keyword from the input
      var userInput = $scope.keyword;

    // fire the API request
    $http.post('/start', {"keyword": userInput}).
        success(function(results) {
          $log.log(results);
          getTweets(results);

        }).
        error(function(error) {
          $log.log(error);
        });

    };

    function getTweets(jobID) {

      var timeout = "";

      var poller = function() {
        // fire another request
        $http.get('/results/'+jobID).
          success(function(data, status, headers, config) {
            if(status === 202) {
              $log.log(data, status);
            } else if (status === 200){
              $log.log(data);
              $scope.tweets = data;
              $timeout.cancel(timeout);
              return false;
            }
            // continue to call the poller() function every 2 seconds
            // until the timeout is cancelled
            timeout = $timeout(poller, 2000);
          });
      };
      poller();
    }
    }
  ]);
}());



