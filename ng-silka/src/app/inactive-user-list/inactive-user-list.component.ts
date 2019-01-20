import {Component, OnInit} from '@angular/core';
import {Observable} from "rxjs";
import {UserService} from "../services/user/user.service";
import {DomSanitizer} from "@angular/platform-browser";
import {MatIconRegistry, MatSnackBar} from "@angular/material";

@Component({
  selector: 'inactive-user-list',
  templateUrl: './inactive-user-list.component.html',
  styleUrls: ['./inactive-user-list.component.scss']
})
export class InactiveUserListComponent implements OnInit {

  displayedColumns: string[] = ['login', 'first_name', 'last_name', 'room', 'admin', 'action'];

  dataSource: Observable<[]>;

  constructor(protected userService: UserService,
              iconRegistry: MatIconRegistry,
              sanitizer: DomSanitizer,
              protected snackbar: MatSnackBar) {
    iconRegistry.addSvgIcon(
      'account-plus',
      sanitizer.bypassSecurityTrustResourceUrl('assets/account-plus.svg'));
  }

  activateUser(user: any) {
    this.userService.activate(user.id).subscribe(() => {
      this.dataSource = this.userService.getInactiveUsers();
      this.openSnackBar('User activated', '');
    });
  }

  openSnackBar(message: string, action: string) {
    this.snackbar.open(message, action, {
      duration: 2000,
      verticalPosition: 'top'
    });
  }

  ngOnInit() {
    this.dataSource = this.userService.getInactiveUsers();
  }
}
