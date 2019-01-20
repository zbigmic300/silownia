import {Component, OnInit} from '@angular/core';
import {UserService} from "../services/user/user.service";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss']
})
export class ChangePasswordComponent implements OnInit {

  form: FormGroup;

  constructor(protected userService: UserService,
              protected fb: FormBuilder,
              protected snackbar: MatSnackBar) {
  }

  ngOnInit() {
    this.form = this.fb.group({
      'old_password': [null, Validators.required],
      'new_password': [null, Validators.required]
    })
  }

  changePassword(form: FormGroup) {
    this.userService.changePassword(JSON.stringify(form.value))
      .subscribe(() => this.openSnackBar('Password changed', ''));
  }

  openSnackBar(message: string, action: string) {
    this.snackbar.open(message, action, {
      duration: 2000,
      verticalPosition: 'top'
    });
  }
}
