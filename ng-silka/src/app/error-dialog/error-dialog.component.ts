import {Component, Inject, OnInit} from '@angular/core';
import {MAT_DIALOG_DATA, MatDialogRef} from "@angular/material";
import {UserService} from "../services/user/user.service";

@Component({
  selector: 'error-dialog',
  templateUrl: './error-dialog.component.html',
  styleUrls: ['./error-dialog.component.scss']
})
export class ErrorDialogComponent implements OnInit {

  errorMsg: string;
  errorStatus: string;

  constructor(public dialogRef: MatDialogRef<ErrorDialogComponent>,
              @Inject(MAT_DIALOG_DATA) public data: any,
              protected userService: UserService) {
  }

  ngOnInit() {
    this.errorMsg = this.data.errorMsg;
    this.errorStatus = this.data.errorStatus;
  }
  close(): void {
    this.dialogRef.close();
  }
}
