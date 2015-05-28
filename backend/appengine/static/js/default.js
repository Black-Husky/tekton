/**
 * Created by Minoru on 28/04/2015.
 */

//-->vars<--

var app = angular.module('App', ['ngMaterial', 'angular-loading-bar', 'ngAnimate']);
var iconsPath = "/static/img/material-design-icons/";

app.factory('Scopes', function ($rootScope) {
    var mem = {};

    return {
        store: function (key, value) {
            $rootScope.$emit('scope.stored', key);
            mem[key] = value;
        },
        get: function (key) {
            return mem[key];
        }
    };
});

app.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
});

//-->Controllers<--
app.controller('AppCtrl', function ($scope, $mdSidenav, $mdDialog, Scopes, $mdToast) {
    $scope.toggleSidenav = function (menuId) {
        $mdSidenav(menuId).toggle();
    };

    Scopes.store('AppCtrl', $scope);

    $scope.alert = '';
    $scope.dialog = '';

    $scope.showActionToast = function (string) {
        var toast = $mdToast.simple()
            .content(string)
            .action('OK')
            .highlightAction(true)
            .theme(true)
            .position("top right");
    };

    $scope.showAdd = function (ev) {
        $scope.dialog = $mdDialog;
        $scope.dialog.show({
            controller: DialogController,
            templateUrl: '/admin/games-management-form-dialog',
            targetEvent: ev
        })
            .then(function (answer) {

            }, function () {

            });
    };

    $scope.showEdit = function (ev, id) {
        $scope.dialog = $mdDialog;
        $scope.dialog.show({
            controller: DialogController,
            templateUrl: '/admin/games-management-form-dialog/' + id,
            targetEvent: ev
        })
            .then(function (answer) {

            }, function () {

            });
    };
});

function DialogController($scope, $mdDialog) {
    $scope.hide = function () {
        $mdDialog.hide();
    };
    $scope.cancel = function () {
        $mdDialog.cancel();
    };
    $scope.answer = function (answer) {
        $mdDialog.hide(answer);
    };
}

app.controller('tableController', function ($scope, $http, Scopes) {

    // $scope will allow this to pass between controller and view
    Scopes.store('tableController', $scope);

    $scope.init = function () {
        $scope.game_list = []
        $http.get("/admin/games-management/list")
            .error(function (data) {
                console.log(data);
            }).success(function (data) {
                //console.log(data);
                $scope.game_list = data;
            });
    }

    $scope.delete = function (ev, id) {
        /*
         var element = $(elm).closest("tr").css("display", "none");
         console.log(element)
         element.css("display", "none");
         element.append("<div class='tr-overlay' style='width:"+element.width+"px; height="+element.height+"px; left:"+element.left+"px; top:"+element.top+"px'></div>");
         */

        // get all the inputs into an array.
        var $inputs = $("#form-" + id + " :input");

        // get an associative array of just the values.
        var values = {};
        $inputs.each(function () {
            values[this.name] = $(this).val();
        });

        $http({
            method: 'POST',
            url: '/admin/games-management/delete',
            data: values,  // pass in data as strings
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}  // set the headers so angular passing info as form data (not request payload)
        })
            .error(function (data, status, headers, config) {
                console.log(data)
            })
            .success(function (data, status, headers, config) {
                $scope.init();
            });
    }
});

// create angular controller and pass in $scope and $http
app.controller('formController', function ($scope, $http, Scopes) {

    // create a blank object to hold our form information
    // $scope will allow this to pass between controller and view
    $scope.formData = {};

    $scope.init = function (id) {
        if (id) {
            $http({
                method: 'POST',
                url: '/admin/games-management/search_id/' + id,
                data: $scope.formData,  // pass in data as strings
                headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}  // set the headers so angular passing info as form data (not request payload)
            })
                .error(function (error) {
                    console.log(error);
                })
                .success(function (data) {
                    $('label').addClass('active')
                    $scope.formData.name = data.name;
                    $scope.formData.nickname = data.nickname;
                    $scope.formData.notes = data.notes;
                    $scope.formData.active = data.active;
                    $scope.formData.game_page = data.game_page;
                    $scope.formData.game_community = data.game_community;
                    $scope.formData.steam_link = data.steam_link;
                    $scope.formData.id = data.id;
                });
        };
    };

    // process the form
    $scope.processForm = function (ev, path) {
        blockForm = function () {
            $(":submit").attr({
                "disabled": "disabled",
                "ng-disabled": true,
                "aria-disabled": true
            });

            $(".validate").removeClass("invalid");
            $(".input-error").text("");

            $(".dialog-overlay").removeClass("dialog-overlay-fade-out").addClass("dialog-overlay-fade-in").on('transitionend webkitTransitionEnd', function (e) {
                //console.log(e.originalEvent.propertyName);
                //console.log(e.originalEvent.elapsedTime + 's');
            });
        }

        resetForm = function () {
            $(":submit").removeAttr("disabled ng-disabled aria-disabled");

            $(".validate").removeClass("invalid valid");
            $(".validate").val("");
            $(".input-error").text("");
            $scope.formData = {};
        }

        blockForm();

        $http({
            method: 'POST',
            url: '/admin/games-management/'+path,
            data: $scope.formData,  // pass in data as strings
            headers: {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}  // set the headers so angular passing info as form data (not request payload)
        })
            .error(function (error) {
                console.log(error);
            })
            .success(function (data) {
                var errors = data['errors']
                if (data.errors) {
                    if (errors['name']) {
                        $("#input-name-error").text(errors['name']);
                        $("input[name='name']").addClass("invalid")
                        $("input[name='name']").focus()
                    }
                    if (errors['nickname']) {
                        $("#input-nickname-error").text(errors['nickname']);
                        $("input[name='nickname']").addClass("invalid")
                        $("input[name='nickname']").focus()
                    }
                } else {
                    // if successful, bind success message to message
                    Scopes.get("tableController").init();
                    $(".dialog-overlay-success").removeClass("dialog-overlay-fade-out");
                    $(".dialog-overlay-success").addClass("dialog-overlay-fade-in")
                    $(".dialog-overlay-success").click(function () {
                        $(this).removeClass("dialog-overlay-fade-in").addClass("dialog-overlay-fade-out");
                        $(this).unbind("click");
                        if(path == "save") {
                            resetForm();
                        }
                    });
                }
            })
            .finally(function () {
                $(".dialog-overlay").removeClass("dialog-overlay-fade-in").addClass("dialog-overlay-fade-out").on('transitionend webkitTransitionEnd', function (e) {
                    //console.log(e.originalEvent.propertyName);
                    //console.log(e.originalEvent.elapsedTime + 's');
                });
                $(":submit").removeAttr("disabled ng-disabled aria-disabled");
            });
    };
});

app.config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .dark();
});

app.config(function ($mdThemingProvider) {
    // Configure a dark theme with primary foreground yellow
    $mdThemingProvider.theme('docs-dark', 'default')
        .primaryPalette('yellow')
        .dark();
});

app.config(function ($mdIconProvider) {
    // Configure URLs for icons specified by [set:]id.
    $mdIconProvider
        .icon('menu', iconsPath + 'ic_menu_48px.svg')
        .icon('more', iconsPath + 'ic_view_module_48px.svg')
        .icon('search', iconsPath + 'ic_search_48px.svg')
        .icon('games', iconsPath + 'ic_games_48px.svg')
        .icon('settings', iconsPath + 'ic_settings_48px.svg')
        .icon('person', iconsPath + 'ic_person_48px.svg')
        .icon('logout', iconsPath + 'ic_exit_to_app_48px.svg')
        .icon('reports', iconsPath + 'ic_assignment_late_48px.svg')
        .icon('person-guest', iconsPath + 'ic_perm_identity_48px.svg')
        .icon('admin', iconsPath + 'ic_supervisor_account_24px.svg')
        .icon('delete', iconsPath + 'ic_delete_48px.svg')
        .icon('description', iconsPath + 'ic_description_48px.svg')
        .icon('edit', iconsPath + 'ic_edit_48px.svg')
        .icon('keyboard-right-arrow', iconsPath + 'ic_keyboard_arrow_right_48px.svg');
    // Register a named icon set of SVGs
});

function logout() {
    $("#form-logout").submit();
}

$('.dropdown-button').dropdown({
        inDuration: 300,
        outDuration: 225,
        constrain_width: false, // Does not change width of dropdown to that of the activator
        hover: false, // Activate on hover
        gutter: 0, // Spacing from edge
        belowOrigin: false, // Displays dropdown below the button
        alignment: 'right'
    }
);