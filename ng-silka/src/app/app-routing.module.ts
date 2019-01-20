import {RouterModule, Routes} from "@angular/router";
import {ReservationCalendarComponent} from "./reservation-calendar/reservation-calendar.component";
import {RegistrationComponent} from "./registration/registration.component";
import {UserComponent} from "./user/user.component";
import {NgModule} from "@angular/core";
import {AppNavigationComponent} from "./app-navigation/app-navigation.component";
import {LoggedUserGuard} from "./user/logged-user.guard";
import {LoginComponent} from "./login/login.component";
import {ChangePasswordComponent} from "./change-password/change-password.component";
import {UserListComponent} from "./user-list/user-list.component";
import {InactiveUserListComponent} from "./inactive-user-list/inactive-user-list.component";


const routes: Routes = [
  {
    path: 'l',
    component: AppNavigationComponent,
    canActivate: [LoggedUserGuard],
    children:
      [
        {
          path: 'calendar',
          component: ReservationCalendarComponent
        },
        {
          path: 'user',
          component: UserComponent
        },
        {
          path: 'register',
          component: RegistrationComponent
        },
        {
          path: 'password',
          component: ChangePasswordComponent
        },
        {
          path: 'user-list',
          component: UserListComponent
        },
        {
          path: 'inactive-user-list',
          component: InactiveUserListComponent
        }
      ]
  },
  {
    path: 'u',
    children:
    [
      {
        path: 'login',
        component: LoginComponent
      },
      {
        path: 'register',
        component: RegistrationComponent
      }
    ]
  },
  {
    path: '',
    redirectTo: '/u/login',
    pathMatch: 'full'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {
}
