import {Component, OnInit} from '@angular/core';
import {CalendarView} from "angular-calendar";
import {
  CalendarEvent,
} from 'calendar-utils';
import {AddReservationDialogComponent} from "../add-reservation-dialog/add-reservation-dialog.component";
import {MatDialog} from "@angular/material";
import {ReservationService} from "../services/reservation/reservation.service";
import {DatePipe, formatDate} from "@angular/common";

@Component({
  selector: 'app-reservation-calendar',
  templateUrl: './reservation-calendar.component.html',
  styleUrls: ['./reservation-calendar.component.scss']
})
export class ReservationCalendarComponent implements OnInit {

  date: Date = new Date();

  view: CalendarView = CalendarView.Week;

  events: CalendarEvent[] = [];/*[
    {
      title: 'Click me',
      color: {primary: 'blue', secondary: 'red'},
      start: new Date()
    },
    {
      title: 'Or click me',
      color: {primary: 'blue', secondary: 'red'},
      start: new Date()
    }
  ];*/

  constructor(protected dialog: MatDialog,
              protected reservationService: ReservationService,
              protected datePipe: DatePipe) {
  }

  ngOnInit() {
    this.reservationService.getWeekReservations()
      .subscribe((reservations: any[]) => {
        this.events = reservations.map(val => {
          return {start: new Date(val.start_date), color: {primary: 'white', secondary: 'white'}, title: val.id}
        });
        console.log(JSON.stringify(this.events));
      })
  }

  addReservation(event: { date: Date }) {
    let startDate: any = event.date;
    let endDate: any = new Date(startDate);
    endDate.setMinutes(startDate.getMinutes() + 59);
    startDate = this.datePipe.transform(startDate, 'yyyy-MM-ddTHH:mm:ss');
    endDate = this.datePipe.transform(endDate, 'yyyy-MM-ddTHH:mm:ss');
    const dialogRef = this.dialog.open(AddReservationDialogComponent, {
      data: {startDate: startDate, endDate: endDate}
    });
    dialogRef.afterClosed().subscribe(result => {
      result && this.reservationService.addReservation(JSON.stringify({start_date: startDate, end_date: endDate}))
        .subscribe()
    });
  }

}
