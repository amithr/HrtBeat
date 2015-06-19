/**
* HrtBeatApp Module
*
* Description
*/
angular.module('hrtBeatApp', [])
	.factory('requestService', ['$http', '$q', function($http, $q) {
		var def = $q.defer();
		return {
			getLinkListAccessKey: function() {
				return $('body').attr('data-link-list-access-key');
			},
			postRequest: function(url, params, errorMsg, callback) {
				params.cache = false;
				$http.post(url, params)
					.success(function(data, status){
						callback(data, status);
					})
					.error(function(data, status){
						callback(data, status)
					});
			}
		}
	}])
	.factory('linkListOperationsService', ['requestService', function(requestService) {
		return {
			retrieveLinkList: function(callback) {
				var url = '/core/retrieve/link-list';
				var params = {linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Failed to get link list.';
				requestService.postRequest(url, params, errorMsg, function(data, status) {
					callback(data, status);
				});
			}
		}
	}])
	.factory('linkOperationsService', ['requestService', function(requestService) {
		return {
			createLink: function(link, callback) {
				var url = '/core/create/link';
				var errorMsg = 'Could not create link.';
				requestService.postRequest(url, link, errorMsg, function(data, status) {
					callback(data, status);
				});
			},
			updateLink: function(link, callback) {
				var url = '/core/update/link';
				var errorMsg = 'Could not update link.';
				requestService.postRequest(url, link, errorMsg, function(data, status) {
					callback(data, status);
				});
			},
			deleteLink: function(linkId, callback) {
				var url = '/core/delete/link';
				var params = {'id': linkId};
				var errorMsg = 'Could not delete link.';
				requestService.postRequest(url, params, errorMsg, function(data, status){
					callback(data, status);
				});
			},
			getSongProvider: function(url) {
				var youtubeKey = 'youtube';
				var soundCloudKey = 'soundcloud';
				if(url.indexOf(youtubeKey) > -1) {
					return 'youtube';
				} else if(url.indexOf(soundCloudKey) > -1) {
					return 'soundcloud';
				} else {
					return 'unknown';
				}
			}
		}
	}])
	.factory('subscriberOperationsService', ['requestService', function(requestService) {
		return {
			createSubscriber: function(subscriberEmail, callback) {
				var url = '/core/add/subscriber';
				var params = {email: subscriberEmail, linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Could not add subscriber';
				requestService.postRequest(url, params, errorMsg, function(data, status){
					callback(data, status);
				});
			},
			deleteSubscriber: function(subscriberId, callback) {
				var url = '/core/delete/subscriber';
				var params = {subscriberId: subscriberId, linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Could not delete subscriber';
				requestService.postRequest(url, params, errorMsg, function(data, status){
					callback(data, status);
				});
			}
		}
	}])
	.controller('LinkListAttributesController', ['$scope', 'linkListOperationsService', 'subscriberOperationsService', function($scope, linkListOperationsService, subscriberOperationsService) {
		//Load link list title
		linkListOperationsService.retrieveLinkList(function(data, status){
			$scope.linkListTitle = data.name;
		});

		$scope.addSubscriber = function() {
			subscriberOperationsService.createSubscriber($scope.subscriberEmail)
		}
	}])
	.controller('LinkListController', ['$scope', 'linkListOperationsService', 'linkOperationsService', 'requestService', function($scope, linkListOperationsService, linkOperationsService, requestService) {
		$scope.links = [];

		$scope.refreshLinkList = function() {
			$("head").append($("<link rel='stylesheet' href='/static/main.css' type='text/css' media='screen' />"));
			$("head").append($("<link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css' />"));
			$("head").append($("<link rel='stylesheet' href='http://yui.yahooapis.com/pure/0.6.0/pure-min.css' />"));
			$scope.links = [];
			//Load all links from db
			linkListOperationsService.retrieveLinkList(function(data, status){
				for(var i = 0; i < data.links.length; i++) {
					$scope.links.push(data.links[i]);
				}
			});
		};

		$scope.refreshLinkList();

		//Add link to db and then refresh link list
		$scope.addLink = function() {
			link = {songUrl: $scope.songUrl, songName: $scope.songName, artistName: $scope.artistName, songProvider: linkOperationsService.getSongProvider($scope.songUrl), linkListAccessKey: requestService.getLinkListAccessKey()};

			linkOperationsService.createLink(link, function(data, status) {
				$scope.refreshLinkList();
			});
			
			$scope.songUrl = '';
			$scope.songName = '';
			$scope.artistName = '';
		}
	}])
	.directive('link', ['linkOperationsService', function(linkOperationsService) {
		return {
			restrict: 'E',
			replace: true,
			scope: {
				linkid: '=',
				songurl: '=',
				songname: '=',
				artistname: '='
			},
			template: 
			'<div class="link" data-link-id="{{linkid}}">' +
				'<p class="artist-name" contenteditable="true">{{artistname}}</p>' +
				'<p class="song-name" contenteditable="true">{{songname}}</p>' +
				'<p class="song-url" contenteditable="true">{{ songurl | limitTo: 20 }}{{songurl.length > 20 ? "..." : ""}}</p>' +
				'<i class="download-link fa fa-download"></i>' +
				'<i class="delete-link fa fa-trash"></i>' +
			'</div>'
			,
			link: function($scope, $http, element) {
				$('.link p').off().on('blur', function(e){
					var $editedFieldLink = $(e.target).parent();
					var link = {};
					link.songUrl = $editedFieldLink.find('.song-url').text();
					link.songName = $editedFieldLink.find('.song-name').text();
					link.artistName = $editedFieldLink.find('.artist-name').text();
					link.id = $editedFieldLink.attr('data-link-id');
					linkOperationsService.updateLink(link, function(data, status){});
					e.preventDefault();
				});

				$('.link i.delete-link').off().on('click', function(e) {
					var $editedFieldLink = $(e.target).parent();
					var $editedFieldLinkContainer = $(e.target).parent().parent();
					var linkId = $editedFieldLink.attr('data-link-id');
					linkOperationsService.deleteLink(linkId, function(data, status){
						$editedFieldLinkContainer.remove();
					})
				});
			}
		}
	}]);


	;