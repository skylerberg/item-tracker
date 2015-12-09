'use strict';

var backend = "http://localhost:5001"

var trackerControllers = angular.module('trackerControllers', []);

trackerControllers.controller('TrackerCtrl', ['$scope', '$http',
  function ($scope, $http) {
    $scope.users = []
    $http.get(backend + "/users").then(function(response) {
      $scope.users = $scope.users.concat(response.data);
    });

    $scope.put_user = function(user) {
      $http.post(backend + "/users", {name: user.name}).then(function(response) {
        $scope.users.push(response.data);
      });
    };

  }
]);

trackerControllers.controller('UserCtrl', ['$scope', '$http', '$routeParams',
  function ($scope, $http, $routeParams) {
    var userId = $routeParams.userId;
    $scope.user = {};
    $scope.users = [];
    $scope.items = [];
    $scope.places = [];
    $scope.tags = [];
    $scope.table = "itemsTable";
    $scope.activeTab = {
      items: "active",
      places: "",
      tags: ""
    };

    $scope.newItem = {};
    $scope.newPlace = {};
    $scope.newTag = {};

    $scope.setActiveTab = function(tabName) {
      $scope.table = tabName + "Table";
      $scope.activeTab.items = tabName === "items" ? "active" : "";
      $scope.activeTab.places = tabName === "places" ? "active" : "";
      $scope.activeTab.tags = tabName === "tags" ? "active" : "";
    };

    $http.get(backend + "/users/" + userId).then(function(response) {
      $scope.user = response.data;
    });

    $http.get(backend + "/users").then(function(response) {
      $scope.users = response.data;
    });

    $http.get(backend + "/users/" + userId + "/items").then(function(response) {
      $scope.items = response.data;
    });

    $http.get(backend + "/users/" + userId + "/places").then(function(response) {
      $scope.places = response.data;
    });

    $scope.post_item = function(item) {
      $http.post(backend + "/users/" + userId + "/items", {
        name: item.name, 
        price: item.price,
        place_id: item.place_id,
      }).then(function(response) {
        $scope.items.push(response.data);
        $scope.newItem = {};
      });
    };

    $scope.putItem = function(item) {
      $http.put(backend + "/users/" + userId + "/items/" + item.id, {
        id: item.id,
        name: item.name, 
        price: item.price,
        place_id: item.place_id,
      }).then(function(response) {
        item.name = response.data["name"];
        item.price = response.data["price"];
        item.place_id = response.data["place_id"];
        item.place_name = response.data["place_name"];
        item.selected = false;
      });
    };

    $scope.reset_item = function(item, index) {
      $http.get(backend + "/users/" + userId + "/items/" + item.id).then(
        function(response) {
          $scope.items[index] = response.data;
        }
      );
    };

    $scope.delete_item = function(index) {
      $http.delete(backend + "/users/" + userId + "/items/" + $scope.items[index].id
          ).then(function(response) {
            $scope.items.splice(index, 1);
      });
    };

    $scope.post_place = function(place) {
      $http.post(backend + "/users/" + userId + "/places", {
        name: place.name, 
      }).then(function(response) {
        $scope.places.push(response.data);
        $scope.newPlace = {};
      });
    };

    $scope.put_place = function(place) {
      $http.put(backend + "/users/" + userId + "/places/" + place.id, {
        id: place.id,
        name: place.name, 
      }).then(function(response) {
        place.name = response.data["name"];
        place.selected = false;
      });
    };

    $scope.reset_place = function(place, index) {
      $http.get(backend + "/users/" + userId + "/places/" + place.id).then(
        function(response) {
          $scope.places[index] = response.data;
        }
      );
    };

    $scope.delete_place = function(index) {
      $http.delete(backend + "/users/" + userId + "/places/" + $scope.places[index].id
          ).then(function(response) {
            $scope.places.splice(index, 1);
      });
    };

    $scope.post_tag = function(tag) {
      $http.post(backend + "/users/" + userId + "/tags", {
        name: tag.name,
        color: tag.color, 
      }).then(function(response) {
        $scope.tags.push(response.data);
        $scope.newTag = {};
      });
    };

    $scope.put_tag = function(tag) {
      $http.put(backend + "/users/" + userId + "/tags/" + tag.id, {
        id: tag.id,
        name: tag.name, 
        color: tag.color, 
      }).then(function(response) {
        tag.name = response.data["name"];
        tag.color = response.data["color"];
        tag.selected = false;
      });
    };

    $scope.reset_tag = function(tag, index) {
      $http.get(backend + "/users/" + userId + "/tags/" + tag.id).then(
        function(response) {
          $scope.tags[index] = response.data;
        }
      );
    };

    $scope.delete_tag = function(index) {
      $http.delete(backend + "/users/" + userId + "/tags/" + $scope.tags[index].id
          ).then(function(response) {
            $scope.tags.splice(index, 1);
      });
    };

    $scope.tagItem = function(item, tag) {
      $http.put(backend + "/users/" + userId + "/items/" + item.id + "/tags/" + tag.id, {}
      ).then(function(response) {
        item.tags = response["data"].tags;
      });
    };

    $scope.getEvents = function(item) {
      $http.get(backend + "/users/" + userId + "/items/" + item.id + "/events").then(
        function(response) {
          item.events = response["data"];
        }
      );
    };

    $http.get(backend + "/users/" + userId + "/tags").then(function(response) {
      $scope.tags = response.data;
    });

    $scope.getItemTemplate = function(item) {
      if (item.selected) {
        return "editItem";
      }
      return "displayItem";
    };

    $scope.getPlaceTemplate = function(place) {
      if (place.selected) {
        return "editPlace";
      }
      return "displayPlace";
    };

    $scope.getTagTemplate = function(tag) {
      if (tag.selected) {
        return "editTag";
      }
      return "displayTag";
    };

  }
]);
