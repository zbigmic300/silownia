import { Component, OnInit } from '@angular/core';
import {UserService} from "../services/user/user.service";
import {Observable} from "rxjs";

@Component({
  selector: 'user-list',
  templateUrl: './user-list.component.html',
  styleUrls: ['./user-list.component.scss']
})
export class UserListComponent implements OnInit {

  displayedColumns: string[] = ['login', 'first_name', 'last_name', 'room', 'admin'];

  dataSource: Observable<[]>;

  constructor(protected userService: UserService) { }

  ngOnInit() {
    this.dataSource = this.userService.getUsers();
  }

}
