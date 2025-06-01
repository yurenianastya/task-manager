import { CommonModule } from '@angular/common';
import { Component, signal, inject, OnInit, Input, SimpleChanges } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { Task, TaskService } from '../../services/task-service';
import { MatIconModule } from '@angular/material/icon';
import { NotificationService } from '../../services/notification-service';
import { BehaviorSubject, combineLatest, filter, Subscription, switchMap, tap } from 'rxjs';
import { MatDialog } from '@angular/material/dialog';
import { EditDialog } from '../edit-dialog/edit-dialog';
import { User } from '../../services/user-service';

@Component({
  selector: 'app-task-list',
  imports: [MatCardModule, CommonModule, MatIconModule],
  templateUrl: './task-list.html',
  styleUrl: './task-list.scss'
})

export class TaskList implements OnInit {
  private taskService = inject(TaskService);
  private notificationService = inject(NotificationService)
  private dialog = inject(MatDialog)

  tasks = signal<Task[]>([]);
  statuses = ['todo', 'in_progress', 'done'];
  private selectedUser$ = new BehaviorSubject<User | null>(null);
  private subscription = new Subscription();

  @Input() set selectedUser(user: User | null) {
    this.selectedUser$.next(user);
  }
  
  ngOnInit() {
    this.notificationService.connectWebSocket();
    const reloadTasks$ = combineLatest([
      this.selectedUser$.pipe(filter(u => u !== null)),
      this.notificationService.messages$
    ]).pipe(
      switchMap(([user]) => this.taskService.getTasks(user!.id)),
      tap(tasks => this.tasks.set(tasks))
    );

    const initialLoad$ = this.selectedUser$.pipe(
      filter(u => u !== null),
      switchMap(user => this.taskService.getTasks(user!.id)),
      tap(tasks => this.tasks.set(tasks))
    );

    this.subscription.add(reloadTasks$.subscribe());
    this.subscription.add(initialLoad$.subscribe());
  }


  filteredTasks(status: string): Task[] {
    return this.tasks().filter(task => task.status === status);
  }

  deleteTask(taskId: number) {
    this.taskService.deleteTask(taskId).subscribe(() => {
      this.tasks.set(this.tasks().filter(task => task.id !== taskId));
    });
  }

  loadTasks(userId: number) {
    this.taskService.getTasks(userId).subscribe(tasks => {
      this.tasks.set(tasks);
    });
  }

  openEditDialog(task: Task) {
    const dialogRef = this.dialog.open(EditDialog, {
      data: { ...task }
    });

    dialogRef.afterClosed().subscribe((result: Task | undefined) => {
      if (result && this.selectedUser$.value) {
        this.taskService.updateTask(result.id, result).subscribe(() => {
          this.loadTasks(this.selectedUser$.value!.id);
        });
      }
    });
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();
  }

}
