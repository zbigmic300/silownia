import {Injectable} from '@angular/core';
import {CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router} from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class LoggedUserGuard implements CanActivate {

  constructor(protected router: Router) {
  }

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): boolean {
    if (sessionStorage.getItem('jwt')) {
      return true;
    }

    // not logged in so redirect to login page with the return url
    this.router.navigate(['/u/login'], { queryParams: { returnUrl: state.url }});
    return false;
  }
}
