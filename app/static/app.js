/**
* HrtBeatApp Module
*
* Description
*/
angular.module('hrtBeatApp', ['ngRoute'])
	.config(function($routeProvider) {
		$routeProvider
			.when('/', {
				templateUrl: '/static/partials/select.html',
				controller: 'WelcomeController'
			})
			.when('/list/:linkListAccessKey', {
				templateUrl: '/static/partials/list.html',
				controller: 'LinkListController'
			})
	})
	.factory('requestService', ['$http', function($http) {
		return {
			postRequest: function(url, params, errorMsg, callback) {
				params.cache = false;
				var req = {
					 method: 'POST',
					 url: url,
					 headers: {
					   'Authentication-Token': 1000
					 },
					 data: params
				}
				$http(req)
					.success(function(data) {
						callback(data);
					})
					.error(function(data) {
						callback(data)
					});
			}
		}
	}])
	.factory('assetsService', ['requestService', function(requestService){
		return {
			addFontAwesomeStylesheet: function() {
				$("head").append($("<link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css' />"));
			},
			addMainStylesheets: function () {
				$("head").append($("<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css' type='text/css' media='screen' />"));
				$("head").append($("<link rel='stylesheet' href='/static/main.css' type='text/css' media='screen' />"));
			}
		}
	}])
	.factory('linkListOperationsService', ['requestService', function(requestService) {
		return {
			addLinkList: function(linkListAccessKey, callback) {
				var url = '/core/create/link-list';
				var params = {linkListAccessKey: linkListAccessKey};
				var errorMsg = 'Failed to add link list.';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);

				});
			},
			retrieveLinkList: function(linkListAccessKey, callback) {
				var url = '/core/retrieve/link-list';
				var params = {linkListAccessKey: linkListAccessKey};
				var errorMsg = 'Failed to get link list.';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			}
		}
	}])
	.factory('linkOperationsService', ['requestService', function(requestService) {
		return {
			createLink: function(link, callback) {
				var url = '/core/create/link';
				var errorMsg = 'Could not create link.';
				requestService.postRequest(url, link, errorMsg, function(data) {
					callback(data);
				});
			},
			updateLink: function(link, callback) {
				var url = '/core/update/link';
				var errorMsg = 'Could not update link.';
				requestService.postRequest(url, link, errorMsg, function(data) {
					callback(data);
				});
			},
			deleteLink: function(linkId, callback) {
				var url = '/core/delete/link';
				var params = {'id': linkId};
				var errorMsg = 'Could not delete link.';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
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
				errorMsg = 'Could not download song.'
				requestService.postRequest(url, params, errorMsg, function(data) {});
			}	
		}
	}])
	.factory('subscriberOperationsService', ['requestService', function(requestService) {
		return {
			createSubscriber: function(subscriberEmail, callback) {
				var url = '/core/add/subscriber';
				var params = {email: subscriberEmail, linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Could not add subscriber';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			},
			deleteSubscriber: function(subscriberId, callback) {
				var url = '/core/delete/subscriber';
				var params = {subscriberId: subscriberId, linkListAccessKey: requestService.getLinkListAccessKey()};
				var errorMsg = 'Could not delete subscriber';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			}
		}
	}])
	.factory('validationService', ['requestService', function(requestService) {
		return {
			isLinkUrlValid: function(linkUrl) {
			},
			isLinkListAccessKeyValid: function(linkListAccessKey) {

			},
			showErrorFlashMessage: function(message) {

			},
			showSuccessFlashMessage: function(message) {

			}
		}
	}])
	.factory('userService', ['$location', 'requestService', function(requestService) {
		return {
			logoutUser: function(params, callback) {
				var url = '/auth/logout';
				var errorMsg = 'Could not logout user';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
					requestService.setAuthenticationToken('');
					$location.path('/');
				});
			},
			getUserData: function(callback) {
				var url = '/auth/retrieve/user';
				var $headerContainer = $('#header');
				var email = $headerContainer.find('#user-email').value();
				var accessToken = $headerContainer.find('#access-token');
				var params = {email: email, access_token: accessToken}
				var errorMsg = 'Could not access user data';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			},
			isUserLoggedIn: function() {
				var isUserLoggedIn = $('#header').find('#is-user-logged-in').val();
				return isUserLoggedIn
				
			},
			ensureUserIsLoggedIn: function() {
				var isUserLoggedIn = this.isUserLoggedIn();
				if(!isUserLoggedIn) {
					$location.path('/');
				}
			}
		}
	}])
	.controller('HeaderController', ['$scope', 'userService', function($scope, userService) {
		$scope.logout = function() {
			params = {};
			$scope.isUserLoggedIn = userService.isUserLoggedIn();
			userService.logoutUser(function(data) {
				$scope.email = '';
				$scope.accessToken = '';
				$scope.isUserLoggedIn = false
			});
		}
	}])
	.controller('WelcomeController', ['$scope', '$location', 'assetsService', 'userService', 'linkListOperationsService', function($scope, $location, assetsService, userService, linkListOperationsService) {
		assetsService.addMainStylesheets();
		$scope.isUserLoggedIn = userService.isUserLoggedIn();
		$scope.linkListAccessKeyExists = false;

		var validateLinkListKey = function(event) {
			linkListOperationsService.retrieveLinkList($scope.linkListAccessKey, function(data) {
				if(data.status) {
					$scope.linkLinkAccessKeyExists = true;
				}
			});
		};

		var redirectToCurrentLinkList = function() {
			var linkListPath = '/list/' + $scope.linkListAccessKey;
			$location.path(linkListPath);
		}

		$scope.selectLinkList = function() {
			redirectToCurrentLinkList();
		};

		$scope.addLinkList = function() {
			if(!$scope.linkListAccessKeyExists) {
				linkListOperationsService.addLinkList($scope.linkListAccessKey, function(data) {
					redirectToCurrentLinkList();
				});
			}
		};
	}])
	.controller('LinkListController', ['$scope', '$routeParams', 'requestService','assetsService', 'linkListOperationsService', 'linkOperationsService', 'providersOperationsService', function($scope, $routeParams, 
																																			requestService, assetsService, linkListOperationsService, linkOperationsService, 
																																			providersOperationsService) {
		
		$scope.links = [];
		assetsService.addFontAwesomeStylesheet();
		assetsService.addMainStylesheets();
		var linkListAccessKey = $routeParams.linkListAccessKey;

		$scope.refreshLinkList = function() {
			assetsService.addFontAwesomeStylesheet();
			assetsService.addMainStylesheets();
			$scope.links = [];
			//Load all links from db
			linkListOperationsService.retrieveLinkList(linkListAccessKey, function(data) {
				if(data.status) {
					for(var i = 0; i < data.links.length; i++) {
						$scope.links.push(data.links[i]);
					}
				}
			});
		};

		$scope.refreshLinkList();

		//Add link to db and then refresh link list
		$scope.addLink = function() {
			link = {songUrl: $scope.songUrl, songTitle: $scope.songTitle, songArtist: $scope.songArtist, songProvider: providersOperationsService.getSongProvider($scope.songUrl), linkListAccessKey: linkListAccessKey};

			linkOperationsService.createLink(link, function(data) {
				$scope.refreshLinkList();
			});
			
			$scope.songUrl = '';
			$scope.songTitle = '';
			$scope.songArtist = '';
		}
	}])
	.directive('link', ['linkOperationsService', 'providersOperationsService', function(linkOperationsService, providersOperationsService) {
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
				'<p class="access-link"><a href="{{songurl}}" target="_blank"><i class="fa fa-arrow-right"></i></a><span class="click-count">{{clickcount}}</span></p>' +
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
					link.id = $linkContainer.attr('data-link-id');
					return link;
				}

				$('.link p').off().on('blur', function(e){
					var $link = $(e.target).parent();
					linkOperationsService.updateLink(getLinkData($link), function(data){});
					e.preventDefault();
				});

				$('.link p.delete-link').off().on('click', function(e) {
					var $link = $(e.target).parent();
					var $linkContainer = $(e.target).parent().parent();
					var linkId = $linkContainer.attr('data-link-id');
					linkOperationsService.deleteLink(linkId, function(data){
						$linkContainer.remove();
					});
					e.preventDefault();
				});

				$('.link p.access-link').off().on('click', function(e) {
					var $link = $(e.target).parent().parent();
					var linkData = getLinkData($link);
					++linkData.clickCount;
					$scope.$apply(function() {
						++$scope.clickcount;
					});
					linkOperationsService.updateLink(linkData, function(data){});
				});

				$('.link p.download-link').off().on('click', function(e) {
					var $link = $(e.target).parent();
					var linkData = getLinkData($link);
					++linkData.downloadCount;
					$scope.$apply(function() {
						++$scope.downloadcount;
					});
					providersOperationsService.downloadSong(linkData);
					linkOperationsService.updateLink(linkData, function(data){});
					e.preventDefault();
				});
			}
		}
	}]);
	;