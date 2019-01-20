import {Injectable} from "@angular/core";
import * as jwt_decode from "jwt-decode";

@Injectable()
export class LoggedUserService {

  get isAdmin(): boolean {
    return this.getDecodedAccessToken(sessionStorage.getItem('jwt'))['identity'] === 'admin';
  }

  getDecodedAccessToken(token: string): any {
    try {
      return jwt_decode(token);
    } catch (Error) {
      return {};
    }
  }
}
