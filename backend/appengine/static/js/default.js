/**
 * Created by Minoru on 28/04/2015.
 */

//-->vars<--
var app = angular.module('StarterApp', ['ngMaterial']);
var iconsPath = "/static/img/material-design-icons/"

//-->Controllers<--
app.controller('AppCtrl', ['$scope', '$mdSidenav', function ($scope, $mdSidenav) {
    $scope.toggleSidenav = function (menuId) {
        $mdSidenav(menuId).toggle();
    };
}]);

/*app.controller('AppCtrl', function ($scope, $mdDialog) {
    $scope.alert = '';
    $scope.showAlert = function (ev) {
        // Appending dialog to document.body to cover sidenav in docs app
        // Modal dialogs should fully cover application
        // to prevent interaction outside of dialog
        $mdDialog.show(
            $mdDialog.alert()
                .parent(angular.element(document.body))
                .title('This is an alert title')
                .content('You can specify some description text in here.')
                .ariaLabel('Alert Dialog Demo')
                .ok('Got it!')
                .targetEvent(ev)
        );
    };
    $scope.showConfirm = function (ev) {
        // Appending dialog to document.body to cover sidenav in docs app
        var confirm = $mdDialog.confirm()
            .parent(angular.element(document.body))
            .title('Would you like to delete your debt?')
            .content('All of the banks have agreed to forgive you your debts.')
            .ariaLabel('Lucky day')
            .ok('Please do it!')
            .cancel('Sounds like a scam')
            .targetEvent(ev);
        $mdDialog.show(confirm).then(function () {
            $scope.alert = 'You decided to get rid of your debt.';
        }, function () {
            $scope.alert = 'You decided to keep your debt.';
        });
    };
    $scope.showAdvanced = function (ev) {
        $mdDialog.show({
            controller: DialogController,
            templateUrl: '/admin/games-management-form-dialog',
            targetEvent: ev
        })
            .then(function (answer) {
                $scope.alert = 'You said the information was "' + answer + '".';
            }, function () {
                $scope.alert = 'You cancelled the dialog.';
            });
    };
});*/

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

app.config(function ($mdThemingProvider) {
    $mdThemingProvider.theme('default')
        .dark();
});

app.config( function($mdThemingProvider){
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