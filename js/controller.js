angular.module('otticode', [])
    .controller('AppCtrl', function($scope) {
        $scope.clickHandler = function() {
        	window.alert('Clicked!');
        }
    });
