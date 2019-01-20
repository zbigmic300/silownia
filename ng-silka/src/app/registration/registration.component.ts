import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {UserService} from "../services/user/user.service";
import {Router} from "@angular/router";
import {MatSnackBar} from "@angular/material";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  form: FormGroup;

  isAdmin: boolean = false;

  constructor(protected fb: FormBuilder,
              protected userService: UserService,
              protected router: Router,
              protected snackbar: MatSnackBar) {

  }

  ngOnInit() {
    this.form = this.fb.group({
      'login': [null, Validators.required],
      'password': [null, Validators.required],
      'first_name': [null],
      'last_name': [],
      'room': [],
    })
  }

  userLogged(){
    return this.router.url.includes('/l/');
  }

  openSnackBar(message: string, action: string) {
    this.snackbar.open(message, action, {
      duration: 2000,
      verticalPosition: 'top'
    });
  }

  register(form: FormGroup) {
    if (this.userLogged()) {
      this.userService.registerAdmin(JSON.stringify(form.value)).subscribe(() => this.openSnackBar('User registered', ''));
    } else {
      this.userService.registerUser(JSON.stringify(form.value)).subscribe(() => this.openSnackBar('User registered', ''));
    }
  }

}
