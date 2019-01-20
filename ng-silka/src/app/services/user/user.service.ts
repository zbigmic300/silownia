import {Injectable} from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {map} from "rxjs/operators";

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(protected http: HttpClient) {
  }

  getUsers(): Observable<[]> {
    return <Observable<[]>>this.http.get('http://localhost:4000/admin/users', {} );
  }

  getInactiveUsers(): Observable<[]> {
    return <Observable<[]>>this.http.get('http://localhost:4000/admin/users?status=W', {} );
  }

  activate(userId: number) {
    return this.http.patch('http://localhost:4000/admin/user/' + userId, {} );
  }

  registerUser(data: any): Observable<any> {
    return this.http.post('http://localhost:4000/user', data, {headers: {'Content-Type': 'application/json'}});
  }

  registerAdmin(data: any): Observable<any> {
    return this.http.post('http://localhost:4000/admin/users', data, {headers: {'Content-Type': 'application/json'}});
  }

  login(data: any): Observable<any> {
    return this.http.post('http://localhost:4000/login', data, {headers: {'Content-Type': 'application/json'}})
      .pipe(
        map(response => {
          sessionStorage.setItem('jwt',response['access_token']);
          sessionStorage.setItem('refresh_token',response['refresh_token']);
        })
      )
  }

  refreshToken() {
    return this.http.post('http://localhost:4000/refresh', null, {headers: {'Content-Type': 'application/json'}})
      .pipe(
        map(response => {
          sessionStorage.setItem('jwt',response['access_token']);
        })
      )
  }

  logout() {
    return this.http.post('http://localhost:4000/logout', {refresh_token: sessionStorage.getItem('refresh_token')}, {headers: {'Content-Type': 'application/json'}})
  }

  changePassword(data: any) {
    return this.http.patch('localhost:4000/login', data, {headers: {'Content-Type': 'application/json'}});
  }
}

