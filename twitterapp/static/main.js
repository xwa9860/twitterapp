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
          startFetch(userInput);
        };

        function startFetch(userInput){
          $http.post('/start', {"keyword": userInput}).
            success(function(results) {
              console.log('foo');
              $log.log(results);
              getTweets(results, userInput);

            }).
            error(function(error) {
              $log.log(error);
            });

        }
        function getTweets(jobID, userInput) {

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
                  startFetch(userInput);
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
    ])
    .directive('sentimentChart', ['$parse', function ($parse) {
      return {
        restrict: 'E',
        replace: true,
        template: '<div id="chart"></div>',
        link: function (scope) {
          scope.$watch('tweets', function() {
            d3.select('#chart').selectAll('*').remove();
            var data = scope.tweets;
            for (var tweet in data) {
              d3.select('#chart')
                .append('div')
                .selectAll('div')
                .data(1)
                .enter()
                .append('div')
                .style('width', 20)
                .text(function(d){
                  return tweet[0];
                });
            }
          }, true);
        }
      };
    }]);

}());



