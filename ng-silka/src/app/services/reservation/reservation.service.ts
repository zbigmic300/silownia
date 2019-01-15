import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";

@Injectable()
export class ReservationService {

  constructor(protected http: HttpClient) { }

  addReservation(data: any){
    return this.http.post('http://localhost:4000/reservations', data, {headers: {'Content-Type': 'application/json'}})
  }

  getReservations() {
    return this.http.get('http://localhost:4000/reservations')
  }

  getWeekReservations() {
    return this.http.get('http://localhost:4000/week/reservations')
  }

}
