import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppComponent} from './app.component';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {AppNavigationComponent} from './app-navigation/app-navigation.component';
import {LayoutModule} from '@angular/cdk/layout';
import {
  MatToolbarModule,
  MatButtonModule,
  MatSidenavModule,
  MatIconModule,
  MatListModule,
  MatMenuModule,
  MatCardModule,
  MatFormFieldModule,
  MatInputModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatRadioModule,
  MatSelectModule,
  MatOptionModule,
  MatSlideToggleModule,
  MatGridListModule,
  MatTooltipModule,
  MatTableModule
} from '@angular/material';
import {ReservationCalendarComponent} from './reservation-calendar/reservation-calendar.component';
import {CalendarModule, DateAdapter} from "angular-calendar";
import {adapterFactory} from "angular-calendar/date-adapters/date-fns";
import {RegistrationComponent} from "./registration/registration.component";
import {UserComponent} from "./user/user.component";
import {ReactiveFormsModule} from "@angular/forms";
import {UserService} from "./services/user/user.service";
import {HTTP_INTERCEPTORS, HttpClientModule} from "@angular/common/http";
import {AppRoutingModule} from "./app-routing.module";
import {DashboardComponent} from './dashboard/dashboard.component';
import {LoginComponent} from './login/login.component';
import {LoggedUserService} from "./user/logged-user.service";
import {ChangePasswordComponent} from './change-password/change-password.component';
import {UserListComponent} from './user-list/user-list.component';
import {AddReservationDialogComponent} from './add-reservation-dialog/add-reservation-dialog.component';
import {ReservationService} from "./services/reservation/reservation.service";
import {AuthInterceptorService} from "./auth-interceptor.service";
import {DatePipe} from "@angular/common";
import { ErrorDialogComponent } from './error-dialog/error-dialog.component';

export const MATERIAL_MODULES = [
  MatButtonModule,
  MatMenuModule,
  MatToolbarModule,
  MatIconModule,
  MatCardModule,
  BrowserAnimationsModule,
  MatFormFieldModule,
  MatInputModule,
  MatDatepickerModule,
  MatNativeDateModule,
  MatRadioModule,
  MatSelectModule,
  MatOptionModule,
  MatSidenavModule,
  MatListModule,
  MatTooltipModule,
  MatSlideToggleModule,
  MatTableModule
];

export const PROVIDERS = [
  UserService,
  LoggedUserService,
  ReservationService,
  DatePipe,
  {provide: HTTP_INTERCEPTORS, useClass: AuthInterceptorService, multi: true},

];

@NgModule({
  declarations: [
    AppComponent,
    AppNavigationComponent,
    ReservationCalendarComponent,
    RegistrationComponent,
    UserComponent,
    DashboardComponent,
    LoginComponent,
    ChangePasswordComponent,
    UserListComponent,
    AddReservationDialogComponent,
    UserListComponent,
    ErrorDialogComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    LayoutModule,
    AppRoutingModule,
    CalendarModule.forRoot({
      provide: DateAdapter,
      useFactory: adapterFactory
    }),
    ReactiveFormsModule,
    ...MATERIAL_MODULES,
    HttpClientModule,
    MatGridListModule,
    MatCardModule,
    MatMenuModule,
    MatIconModule,
    MatButtonModule
  ],
  providers: [...PROVIDERS],
  bootstrap: [AppComponent],
  entryComponents: [AddReservationDialogComponent, ErrorDialogComponent]
})
export class AppModule {
}
