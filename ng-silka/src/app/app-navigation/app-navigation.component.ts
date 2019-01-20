import { Component } from '@angular/core';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import {UserService} from "../services/user/user.service";
import {Router} from "@angular/router";
import {LoggedUserService} from "../user/logged-user.service";

@Component({
  selector: 'app-navigation',
  templateUrl: './app-navigation.component.html',
  styleUrls: ['./app-navigation.component.scss']
})
export class AppNavigationComponent {

  isHandset$: Observable<boolean> = this.breakpointObserver.observe(Breakpoints.Handset)
    .pipe(
      map(result => result.matches)
    );

  constructor(private breakpointObserver: BreakpointObserver,
              protected userService: UserService,
              protected router: Router,
              protected loggedUserService: LoggedUserService) {
  }

  isAdmin(){
    return this.loggedUserService.isAdmin;
  }

  logout(){
    this.userService.logout().subscribe(res => {
      sessionStorage.clear();
      this.router.navigate(['/u/login']);
    });
  }
}
