import { Component, EventEmitter, inject, Output } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatFormFieldModule } from '@angular/material/form-field';
import { User, UserService } from '../../services/user-service';
import { MatOptionModule } from '@angular/material/core';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { NotificationService } from '../../services/notification-service';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatDialog } from '@angular/material/dialog';
import { EditDialog } from '../edit-dialog/edit-dialog';
import { Task, TaskService } from '../../services/task-service';

@Component({
  selector: 'app-header',
  imports: [
    MatToolbarModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatOptionModule,
    MatSelectModule,
    FormsModule,
    MatTooltipModule,
    CommonModule
  ],
  templateUrl: './header.html',
  styleUrl: './header.scss'
})
export class Header {
  private userService = inject(UserService);
  private taskService = inject(TaskService);
  private notificationService = inject(NotificationService);
  private dialog = inject(MatDialog);
  
  users: User[] = [];
  selectedUser: User | undefined;

  @Output() userChanged = new EventEmitter<User>();

  ngOnInit() {
    this.userService.getUsers().subscribe(users => {
      this.users = users;
      this.selectedUser = users[0];
      this.userChanged.emit(this.selectedUser);
      this.notificationService.connectWebSocket();
      this.notificationService.getNotifications().subscribe(msg => {
        if (msg.includes('User')) {
          this.userService.getUsers().subscribe(users => {
            this.users = users;
          });
        }
      });
    });
  }
  
  onUserChanged(event: MatSelectChange) {
    const selectedUser = event.value as User;
    this.selectedUser = selectedUser;
    if (this.selectedUser) {
      this.userChanged.emit(this.selectedUser);
    }
  }

  openEditDialog(task?: Task) {
    const dialogRef = this.dialog.open(EditDialog, {
      data: { task, user_id: this.selectedUser?.id }
    });

    dialogRef.afterClosed().subscribe((result: Task | undefined) => {
      if (result) {
        const payload = {
          ...result,
          user_id: this.selectedUser?.id || result.user_id
        };
        this.taskService.createTask(payload).subscribe();
      }
    });
  }

}
