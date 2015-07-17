/**
* HrtBeatApp Module
*
* Description
*/
angular.module('hrtBeatApp', [])
	.factory('requestService', ['$http', function($http) {
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
	.factory('coreOperationsService', ['requestService', function(requestService) {
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
			}
		}
	}])
	.factory('providersOperationsService', ['requestService', function(requestService) {
		return {
			getSongProvider: function(url) {
				var youtubeKey = 'youtube';
				var soundCloudKey = 'soundcloud';
				var beatPortKey = 'beatport';
				if(url.indexOf(youtubeKey) > -1) {
					return youtubeKey;
				} else if(url.indexOf(soundCloudKey) > -1) {
					return soundCloudKey;
				} else if(url.indexOf(beatPortKey) > -1) {
					return beatPortKey
				} else {
					return 'unknown';
				}	
			},
			getDownloadableSongProviders: function() {
				return ['youtube']
			},
			downloadSong: function(link) {
				var url = '/providers/download/song'
				var params = {provider: this.getSongProvider(link.songUrl), url: link.songUrl, artist: link.songArtist, title: link.songTitle}
				requestService.postRequest(url, params, function(data, status) {});
			}	
		}
	}])
	.factory('subscriberOperationsService', ['requestService', function(requestService) {
		return {
			createSubscriber: function(subscriberEmail, callback) {
				var url = '/core/add/subscriber';
				var params = {email: subscriberEmail, linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Could not add subscriber';
				requestService.postRequest(url, params, errorMsg, function(data, status) {
					callback(data, status);
				});
			},
			deleteSubscriber: function(subscriberId, callback) {
				var url = '/core/delete/subscriber';
				var params = {subscriberId: subscriberId, linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Could not delete subscriber';
				requestService.postRequest(url, params, errorMsg, function(data, status) {
					callback(data, status);
				});
			}
		}
	}])
	.controller('LinkListAttributesController', ['$scope', 'linkListOperationsService', 'subscriberOperationsService', function($scope, linkListOperationsService, subscriberOperationsService) {
		//Load link list title
		linkListOperationsService.retrieveLinkList(function(data, status) {
			$scope.linkListTitle = data.name;
			$scope.subscriberCount = data.subscriberCount;
		});

		$scope.addSubscriber = function() {
			subscriberOperationsService.createSubscriber($scope.subscriberEmail)
		}
	}])
	.controller('LinkListController', ['$scope', 'linkListOperationsService', 'coreOperationsService', 'providersOperationsService', 'requestService', function($scope, linkListOperationsService, coreOperationsService, providersOperationsService, requestService) {
		$scope.links = [];

		$scope.refreshLinkList = function() {
			$("head").append($("<link rel='stylesheet' href='/static/main.css' type='text/css' media='screen' />"));
			$("head").append($("<link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css' />"));
			$("head").append($("<link rel='stylesheet' href='http://yui.yahooapis.com/pure/0.6.0/pure-min.css' />"));
			$scope.links = [];
			//Load all links from db
			linkListOperationsService.retrieveLinkList(function(data, status) {
				for(var i = 0; i < data.links.length; i++) {
					$scope.links.push(data.links[i]);
				}
			});
		};

		$scope.refreshLinkList();

		//Add link to db and then refresh link list
		$scope.addLink = function() {
			link = {songUrl: $scope.songUrl, songTitle: $scope.songTitle, songArtist: $scope.songArtist, songProvider: providersOperationsService.getSongProvider($scope.songUrl), linkListAccessKey: requestService.getLinkListAccessKey()};

			coreOperationsService.createLink(link, function(data, status) {
				$scope.refreshLinkList();
			});
			
			$scope.songUrl = '';
			$scope.songTitle = '';
			$scope.songArtist = '';
		}
	}])
	.directive('link', ['coreOperationsService', 'providersOperationsService', function(coreOperationsService, providersOperationsService) {
		return {
			restrict: 'E',
			replace: true,
			scope: {
				linkid: '=',
				songurl: '=',
				songtitle: '=',
				songartist: '=',
				clickcount: '=',
				downloadcount: '='
			},
			template: 
			'<div class="link" data-link-id="{{linkid}}">' +
				'<p class="song-artist" contenteditable="true">{{songartist}}</p>' +
				'<p class="song-title" contenteditable="true">{{songtitle}}</p>' +
				'<p class="song-url" contenteditable="true">{{songurl}}</p>' +
				'<p class="access-link"><a href="{{songurl}}"><i class="fa fa-arrow-right"></i></a><span class="click-count">{{clickcount}}</span></p>' +
				'<p class="download-link"><i class="fa fa-download"></i><span class="download-count">{{downloadcount}}</span></p>' +
				'<p class="delete-link"><i class="fa fa-trash"></i></p>' +
			'</div>'
			,
			link: function($scope, $http, element) {
				function getLinkData($link) {
					var $linkContainer = $link.parent();
					var link = {};
					link.songUrl = $linkContainer.find('.song-url').text();
					link.songTitle = $linkContainer.find('.song-title').text();
					link.songArtist = $linkContainer.find('.song-artist').text();
					link.clickCount = $linkContainer.find('.click-count').text();
					link.downloadCount = $linkContainer.find('.download-count').text();
					link.id = $link.attr('data-link-id');
					return link;
				}

				$('.link p').off().on('blur', function(e){
					var $link = $(e.target).parent();
					coreOperationsService.updateLink(getLinkData($link), function(data, status){});
					e.preventDefault();
				});

				$('.link p.delete-link').off().on('click', function(e) {
					var $link = $(e.target).parent();
					var $linkContainer = $(e.target).parent().parent();
					var linkId = $link.attr('data-link-id');
					coreOperationsService.deleteLink(linkId, function(data, status){
						$linkContainer.remove();
					});
					e.preventDefault();
				});

				$('.link p.download-link').off().on('click', function(e) {
					var $link = $(e.target).parent().parent();
					var linkData = getLinkData($link)
					++$scope.downloadcount;
					++linkData.downloadCount;
					providersOperationsService.downloadSong(linkData);
					coreOperationsService.updateLink(linkData, function(data, status){});
					e.preventDefault();
				});
			}
		}
	}]);
	;