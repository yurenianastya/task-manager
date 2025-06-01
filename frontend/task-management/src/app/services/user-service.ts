import { inject, Injectable } from '@angular/core';
import { Task } from './task-service';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface User {
  id: number;
  name: string;
  tasks: Task[];
}

export interface CreateUser {
  name: string;
}

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private http = inject(HttpClient);
  private userApi = 'http://localhost:8000/users';

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.userApi);
  }

  getUser(userId: number): Observable<User> {
    return this.http.get<User>(`${this.userApi}/${userId}`);
  }

  createUser(user: CreateUser): Observable<User> {
    return this.http.post<User>(this.userApi, user);
  }

  deleteUser(userId: number): Observable<any> {
    return this.http.delete(`${this.userApi}/${userId}`);
  }
}
