import {Injectable} from "@angular/core";


@Injectable()
export class LoggedUserService {
  protected _userLogged: boolean = true;

  get isUserLogged(): boolean{
    return this._userLogged;
  }

  authenticateUser(){

  }
}
