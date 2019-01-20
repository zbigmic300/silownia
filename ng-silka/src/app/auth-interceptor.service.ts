import {Injectable} from '@angular/core';
import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
  HttpResponse
} from "@angular/common/http";
import {Observable, of, throwError} from "rxjs";
import {catchError, map} from "rxjs/operators";
import {UserService} from "./services/user/user.service";
import {Router} from "@angular/router";
import {AddReservationDialogComponent} from "./add-reservation-dialog/add-reservation-dialog.component";
import {MatDialog} from "@angular/material";
import {ErrorDialogComponent} from "./error-dialog/error-dialog.component";

@Injectable()
export class AuthInterceptorService implements HttpInterceptor {

  constructor(protected userService: UserService,
              protected dialog: MatDialog,
              protected router: Router) {
  }

  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // add authorization header with jwt token if available
    if (request.url.includes('/refresh')) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${sessionStorage.refresh_token}`
        }
      });
    } else if (!request.url.includes('/login') && sessionStorage.jwt) {
      request = request.clone({
        setHeaders: {
          Authorization: `Bearer ${sessionStorage.jwt}`
        }
      });
    }
    return next.handle(request).pipe(
      map((event: HttpEvent<any>) => {
        if (event instanceof HttpResponse) {
        }
        return event;
      }),
      catchError((error: HttpErrorResponse) => {
        if (error.status == 401 && !error.url.includes('/refresh')) {
          this.userService.refreshToken().subscribe();
        } else if (error.status == 401 && error.url.includes('/refresh')) {
          this.router.navigate(['u', 'login']);
          sessionStorage.clear();
        }
        console.log(JSON.stringify(error.error));
        const dialogRef = this.dialog.open(ErrorDialogComponent, {
          data: {errorMsg: error.error['message'] ? error.error['message'] : error.error['msg'], errorStatus: error.status}
        });
        return of(null);
      }));
  }
}
