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
				controller: 'ControlPanelController'
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
	.factory('assetsService', ['requestService', function(requestService) {
		return {
			addFontAwesomeStylesheet: function() {
				$("head").append($("<link rel='stylesheet' href='//maxcdn.bootstrapcdn.com/font-awesome/4.3.0/css/font-awesome.min.css' />"));
			},
			addMainStylesheets: function () {
				$("head").append($("<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css' type='text/css' media='screen' />"));
				$("head").append($("<link rel='stylesheet' href='/static/main.css' type='text/css' media='screen' />"));
			},
			addNotificationStyle: function() {
				$.notify.addStyle('standard', {
					html: "<div><span data-notify-text/></div>",
					classes: {
						base: {
							"white-space": "nowrap",
							"background-color": "grey",
							"color": "white",
							"border-radius": "10px",
							"opacity": "0.8",
							"padding": "10px"
						}
					}
				});
			}
		}
	}])
	.factory('linkListOperationsService', ['$location', 'requestService', 'userService', function($location, requestService, userService) {
		return {
			createLinkList: function(params, callback) {
				var url = '/core/create/link-list';
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
			},
			retrieveAndRedirectToLinkList: function(linkListAccessKey) {
				this.retrieveLinkList(linkListAccessKey, function(data) {
					if(data.status) {
						var linkListPath = '/list/' + linkListAccessKey;
						$location.path(linkListPath);
					} else {
						$location.path('/');
					}
				});
			},
			retrieveLinkListsByUser: function(userId, callback) {
				var url = '/core/retrieve/user/link-lists';
				var params = {id: userId};
				var errorMsg = 'Failed to get link list.';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			},
			updateLinkList: function(params, callback) {
				var url = '/core/update/link-list';
				var errorMsg = 'Failed to update link list';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			},
			deleteLinkList: function(linkListAccessKey, callback) {
				var url = '/core/delete/link-list';
				var params = {linkListAccessKey: linkListAccessKey};
				var errorMsg = 'Failed to get link list.';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
				});
			},
			setEditableStateOnLinkList: function(isLinkListEditable) {
				var $linkListContainer = $('#link-list')
				if(isLinkListEditable) {
					$linkListContainer.find('.add-btn').show();
				} else {
					$linkListContainer.find('.add-btn').hide();
				}
			}, 
			generateShareableLink: function(linkListAccessKey) {
				var userData = userService.getUserDataFromClient();
				var host = 'http://localhost:5000';
				var userEmail = userData['email'];
				var url = host + '/core/' + userEmail + '#/list/' + linkListAccessKey;
				return url;
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
	.factory('providersOperationsService', ['requestService', 'userService', function(requestService, userService) {
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
			downloadSong: function(link, callback) {
				var url = '/providers/download/song'
				var userData = userService.getUserDataFromClient();
				var params = {provider: this.getSongProvider(link.songUrl), userEmail: userData['email'], url: link.songUrl, artist: link.songArtist, title: link.songTitle}
				errorMsg = 'Could not download song.'
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data.status);
				});
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
	.factory('userService', ['$location', 'requestService', function($location, requestService) {
		return {
			logoutUser: function(params, callback) {
				var url = '/auth/logout/';
				var errorMsg = 'Could not logout user';
				requestService.postRequest(url, params, errorMsg, function(data) {
					callback(data);
					window.location = '/core';
				});
			},
			getUserDataFromDom: function() {
				var $headerContainer = $('#header');
				var isUserLoggedIn = $headerContainer.find('#is-user-logged-in').val().trim();
				var id = $headerContainer.find('#user-id').val();
				var email = $headerContainer.find('#email').val();
				var name = $headerContainer.find('#name').val();
				var accessToken = $headerContainer.find('#access-token').val();
				var provider = $headerContainer.find('#provider').val();
				var userData = {id: id, email: email, accessToken: accessToken, provider: provider, isUserLoggedIn: isUserLoggedIn};
				return userData
			},
			clearUserDataFromDom: function() {
				var $headerContainer = $('#header');
				var id = $headerContainer.find('#user-id').val('')
				var email = $headerContainer.find('#email').val('');
				var name = $headerContainer.find('#name').val('');
				var accessToken = $headerContainer.find('#access-token').val('');
				var provider = $headerContainer.find('#provider').val('');
			},
			getUserDataFromClient: function() {
				var isUserLoggedIn = $('#header').find('#is-user-logged-in').val().trim();
				if(isUserLoggedIn == 'true') {
					var userData = this.getUserDataFromDom();
					return userData;
				} else {
					$location.path('/');
					//Flash message and redirect (you must be logged in)
				}
			},
			addUserAuthenticationDataToRequestParameters: function(params) {
				var userData = this.getUserDataFromClient();
				return $.extend(params, userData);
			},
			isUserLoggedIn: function() {
				var isUserLoggedInFromDom = $('#header').find('#is-user-logged-in').val().trim();
				if(isUserLoggedInFromDom == 'true') {
					return true;
				} else {
					return false;
				}
			},
			ensureUserIsLoggedIn: function() {
				var isUserLoggedIn = this.isUserLoggedIn();
				if(!isUserLoggedIn) {
					$location.path('/');
				}
			}
		}
	}])
	.controller('HeaderController', ['$scope', '$location', 'userService', function($scope, $location, userService) {
		$scope.isUserLoggedIn = userService.isUserLoggedIn();
		var userData = userService.getUserDataFromClient();

		//Facebook API appends _=_ to url upon login redirect
		if($location.path() == '/_=_') {
			$location.path('/');
		}

		$scope.logout = function() {
			var userData = userService.getUserDataFromClient();
			if(userData) {
				var params = {email: userData["email"], provider: userData["provider"]};
				$scope.isUserLoggedIn = userService.isUserLoggedIn();
				userService.logoutUser(params, function(data) {
					$scope.isUserLoggedIn = false;
					userService.clearUserDataFromDom();
				});
			}
		}
	}])
	.controller('ControlPanelController', ['$scope', '$location', 'assetsService', 'userService', 'linkListOperationsService', function($scope, $location, assetsService, userService, linkListOperationsService) {
		assetsService.addMainStylesheets();
		assetsService.addFontAwesomeStylesheet();
		assetsService.addNotificationStyle();
		$scope.isUserLoggedIn = userService.isUserLoggedIn();
		$scope.linkListAccessKeyExists = false;
		$scope.linkLists = [];
		var userData = userService.getUserDataFromClient();

		$scope.loadLinkLists = function() {
			if(userData) {
				linkListOperationsService.retrieveLinkListsByUser(userData["id"], function(data) {
					if(data.status) {
						for(var i = 0; i < data.linkLists.length; i++) {
							$scope.linkLists.push(data.linkLists[i]);
						}
					}
				});
			}
		}

		$scope.loadLinkLists();

		$scope.selectLinkList = function() {
			linkListOperationsService.retrieveAndRedirectToLinkList($scope.linkListAccessKey);
		}

		$scope.createLinkList = function() {
			if(!$scope.linkListAccessKeyExists && userData) {
				params = {linkListAccessKey: $scope.linkListAccessKey, adminUserId: userData["id"]};
				linkListOperationsService.createLinkList(params, function(data) {
					$scope.selectLinkList();
				});
			}
		};
	}])

	.controller('LinkListController', ['$scope', '$routeParams', '$location', '$timeout', 'requestService','assetsService', 'linkListOperationsService', 'linkOperationsService', 'providersOperationsService', 'userService', function($scope, $routeParams, $location, $timeout,
																																			requestService, assetsService, linkListOperationsService, linkOperationsService, 
																																			providersOperationsService, userService) {
		
		$scope.links = [];
		assetsService.addFontAwesomeStylesheet();
		assetsService.addMainStylesheets();
		assetsService.addNotificationStyle();
		var linkListAccessKey = $routeParams.linkListAccessKey;

		$scope.refreshLinkList = function() {
			assetsService.addFontAwesomeStylesheet();
			assetsService.addMainStylesheets();
			$scope.links = [];
			//Load all links from db
			linkListOperationsService.retrieveLinkList(linkListAccessKey, function(data) {
				if(data.status) {
					linkListOperationsService.setEditableStateOnLinkList(data.editable);
					for(var i = 0; i < data.links.length; i++) {
						data.links[i].editable = data.editable
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
		}, 

		$scope.returnToControlPanel = function() {
			$location.path('/');
		}
	}])
	.directive('linklist', ['linkListOperationsService', 'assetsService', function(linkListOperationsService, assetsService) {
		return {
			restrict: 'E',
			replace: true,
			scope: {
				linklistid: '=',
				linklistaccesskey: '=',
				editable: '='
			},
			template: '<div class="link-list">' +
				'<p class="link-list-access-key hover" contenteditable="true">{{linklistaccesskey}}</p>' +
				'<p class="access-link-list"><i class="fa fa-arrow-right"></i></p>' +
				'<p class="delete-link-list"><i class="fa fa-trash"></i></p>' +
				'<p class="share-link-list"><i class="fa fa-share-alt"></i></p>' +
				'<p class="is-link-list-editable" data-is-link-list-editable={{editable}}><i class="fa fa-edit"></i></p>' +
			'</div>'
			,
			link: function($scope, $http, element) {
				assetsService.addNotificationStyle();

				var getLinkListElements = function($linkList) {
					var linkListElements = {};
					linkListElements.linkListAccessKeyElement = $linkList.find('.link-list-access-key');
					linkListElements.editableElement = $linkList.find('.is-link-list-editable');
					return linkListElements;
				};

				$('.link-list p.access-link-list i').off().on('click', function(e) {
					var $linkList = $(e.target).parent().parent();
					var linkListAccessKey = $linkList.find('.link-list-access-key').text();
					linkListOperationsService.retrieveAndRedirectToLinkList(linkListAccessKey);
				});

				$('.link-list p.delete-link-list i').off().on('click', function(e) {
					var $linkList = $(e.target).parent().parent();
					var linkListAccessKey = $linkList.find('.link-list-access-key').text();
					linkListOperationsService.deleteLinkList(linkListAccessKey, function(data){
						$linkList.remove();
						$.notify('Link list deleted', {
							style: "standard",
							className: "base"
						});
					});
				});

				$('.link-list p.share-link-list i').off().on('click', function(e) {
					var clipboard = new Clipboard('.link-list p.share-link-list i', {
						text: function(triggerElement) {
							var $linkList = $(triggerElement).parent().parent();
							var linkListAccessKey = $linkList.find('.link-list-access-key').text();
							return linkListOperationsService.generateShareableLink(linkListAccessKey);
						}
					});

					clipboard.on('success', function(e) {
						$.notify('Link copied to clipboard', {
							style: "standard",
							className: "base"
						});
						clipboard.destroy();
					});
				});

				$scope.$watch('editable', function() {
					var editableElements = $('.link-list p.is-link-list-editable i');
					editableElements.each(function() {
						var linkListElements = getLinkListElements($(this).parent().parent());
						currentEditableState = linkListElements['editableElement'].attr('data-is-link-list-editable');
						if(currentEditableState == "true") {
							$(this).css('color', '#08e004');
						} else {
							$(this).css('color', 'red');
						}
					});
				});

				$('.link-list p.is-link-list-editable i').off().on('click', function(e) {
					$currentElement = $(e.target);
					var $linkList = $currentElement.parent().parent();
					var linkListElements = getLinkListElements($linkList);
					var currentEditableState = linkListElements['editableElement'].attr('data-is-link-list-editable');
					var updateLinkListParameters = {'linkListAccessKey': linkListElements['linkListAccessKeyElement'].text(), 'editable': currentEditableState};
					if(currentEditableState == "true") {
						linkListElements['editableElement'].attr('data-is-link-list-editable', "false");
						updateLinkListParameters.editable = false;
						$currentElement.css('color', 'red');
						$.notify('Link list is no longer publicly editable', {
							style: "standard",
							className: "base"
						});
					} else {
						linkListElements['editableElement'].attr('data-is-link-list-editable', "true");
						updateLinkListParameters.editable = true;
						$currentElement.css('color', '#08e004');
						$.notify('Link list is now publicly editable', {
							style: "standard",
							className: "base"
						});
					}
					linkListOperationsService.updateLinkList(updateLinkListParameters, function(data){});
				});
			}
		}

	}])
	.directive('link', ['linkOperationsService', 'linkListOperationsService', 'assetsService', 'providersOperationsService', function(linkOperationsService, linkListOperationsService, assetsService, providersOperationsService) {
		return {
			restrict: 'E',
			replace: true,
			scope: {
				linkid: '=',
				songurl: '=',
				songtitle: '=',
				songartist: '=',
				clickcount: '=',
				downloadcount: '=',
				editable: '='
			},
			template: 
			'<div class="link" data-link-id="{{linkid}}">' +
				'<p class="song-artist hover" contenteditable="{{editable}}">{{songartist}}</p>' +
				'<p class="song-title hover" contenteditable="{{editable}}">{{songtitle}}</p>' +
				'<p class="song-url hover" contenteditable="{{editable}}">{{songurl}}</p>' +
				'<p class="access-link"><a href="{{songurl}}" target="_blank"><i class="fa fa-arrow-right"></i></a><span class="click-count">{{clickcount}}</span></p>' +
				'<p class="download-link"><i class="fa fa-download"></i><span class="download-count">{{downloadcount}}</span></p>' +
				'<p class="delete-link"><i class="fa fa-trash"></i></p>' +
			'</div>'
			,
			link: function($scope, $http, element) {
				assetsService.addNotificationStyle();

				function getLinkData($link) {
					var $linkContainer = $link.parent();
					var link = {};
					link.songUrl = $linkContainer.find('.song-url').text();
					link.songTitle = $linkContainer.find('.song-title').text();
					link.songArtist = $linkContainer.find('.song-artist').text();
					link.clickCount = $linkContainer.find('.click-count').text();
					link.downloadCount = $linkContainer.find('.download-count').text();
					linkIdFromDom = $link.attr('data-link-id');
					if(linkIdFromDom) {
						link.id = linkIdFromDom;
					} else {
						link.id = $linkContainer.attr('data-link-id');
					}
					return link;
				}

				$('.link p').off().on('blur', function(e) {
					var $link = $(e.target).parent();
					linkOperationsService.updateLink(getLinkData($link), function(data){});
					e.preventDefault();
				});

				$('.link p.delete-link').off().on('click', function(e) {
					var $link = $(e.target).parent();
					var $linkContainer = $(e.target).parent().parent();
					var linkData = getLinkData($link);
					var linkId = $linkContainer.attr('data-link-id');
					linkOperationsService.deleteLink(linkId, function(data){
						$linkContainer.remove();
						$.notify('Link deleted', {
							style: "standard",
							className: "base"
						});
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
					providersOperationsService.downloadSong(linkData, function(isDownloadPossible) {
						if(!isDownloadPossible) {
							$(e.target).parent().animate({ "border-color":"red"},"fast");
							$.notify('This track cannot be downloaded', {
								style: "standard",
								className: "base"
							});
						} else {
							$(e.target).parent().animate({ "border-color":"#08e004)"},"fast");
							$.notify('A download link to this track has been sent to your email inbox', {
								style: "standard",
								className: "base"
							});
						}
						$(e.target).parent().animate({ "border-color":"rgba(178, 178, 178, 0.3)"},3000);
					});
					linkOperationsService.updateLink(linkData, function(data){});
					e.preventDefault();
				});
			}
		}
	}]);
	;