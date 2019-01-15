import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material";
import {FormBuilder, FormGroup, Validators} from "@angular/forms";
import {UserService} from "../services/user/user.service";

@Component({
  selector: 'add-reservation-dialog',
  templateUrl: './add-reservation-dialog.component.html',
  styleUrls: ['./add-reservation-dialog.component.scss']
})
export class AddReservationDialogComponent implements OnInit {

  startDate: Date;
  endDate: Date;

  constructor(public dialogRef: MatDialogRef<AddReservationDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              protected userService: UserService) {
  }

  ngOnInit() {
    this.startDate = this.data['startDate'];
    this.endDate = this.data['endDate'];
  }

  close(): void {
    this.dialogRef.close();
  }

  add() {
    this.dialogRef.close(true)
  }
}
