import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";
import {UserService} from "../services/user/user.service";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {

  form: FormGroup;

  isAdmin: boolean = false;

  constructor(protected fb: FormBuilder,
              protected userService: UserService) {

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

  register(form: FormGroup) {
    if (this.isAdmin) {
      this.userService.registerAdmin(JSON.stringify(form.value));
    } else {
      this.userService.registerUser(JSON.stringify(form.value));

    }
  }

}
