import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {UserService} from "../services/user/user.service";
import {ActivatedRoute, Router} from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  form: FormGroup;

  constructor(protected fb: FormBuilder,
              protected userService: UserService,
              protected router: Router) {

  }

  ngOnInit() {
    this.form = this.fb.group({
      'login': [null, Validators.required],
      'password': [null, Validators.required]
    })
  }

  login(form: FormGroup) {
    this.userService.login(JSON.stringify(form.value))
      .subscribe( val => this.router.navigate(['/l/calendar']));
  }

}
