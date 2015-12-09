'use strict';

var trackerApp = angular.module('trackerApp', [
  'ngRoute',
  'trackerControllers'
]);


trackerApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/home', {
        templateUrl: 'partials/home.html',
        controller: 'TrackerCtrl'
      }).
      when('/user/:userId', {
        templateUrl: 'partials/user.html',
        controller: 'UserCtrl'
      }).
      otherwise({
        redirectTo: '/home'
      });
  }]);
