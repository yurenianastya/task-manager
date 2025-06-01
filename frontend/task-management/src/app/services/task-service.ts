import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export type Status = 'todo' | 'in_progress' | 'done';
export type Priority = 'low' | 'medium' | 'high';

export interface Task {
  id: number;
  title: string;
  description: string;
  status: Status;
  priority: Priority;
  user_id: number;
}

export interface CreateTask {
  title: string;
  description: string;
  status: Status;
  priority: Priority;
  user_id: number;
}

@Injectable({ providedIn: 'root' })
export class TaskService {
  private http = inject(HttpClient);
  private taskApi = 'http://localhost:8000/tasks';
  
  getTasks(userId?: number): Observable<Task[]> {
    let url = this.taskApi;
    if (userId) url += `?user_id=${userId}`;
    return this.http.get<Task[]>(url);
  }


  createTask(task: CreateTask): Observable<Task> {
    return this.http.post<Task>(this.taskApi, task);
  }

  updateTask(taskId: number, task: CreateTask): Observable<any> {
    return this.http.put(`${this.taskApi}/${taskId}`, task);
  }

  deleteTask(taskId: number): Observable<any> {
    return this.http.delete(`${this.taskApi}/${taskId}`);
  }
}