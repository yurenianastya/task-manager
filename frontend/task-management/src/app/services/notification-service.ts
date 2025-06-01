import { Injectable, inject } from '@angular/core';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, Subject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class NotificationService {

  private snackBar = inject(MatSnackBar);
  private ws: WebSocket | null = null;
  private messageSubject = new Subject<string>();
  public messages$ = this.messageSubject.asObservable();

  connectWebSocket() {
    if (this.ws) return;

    this.ws = new WebSocket('ws://localhost:8000/ws/notifications');
    this.ws.onmessage = (event) => {
      this.snackBar.open(event.data, 'Dismiss', { duration: 3000 });
      this.messageSubject.next(event.data);
    }
    this.ws.onclose = () => this.ws = null;
  }

  closeWebSocket() {
    this.ws?.close();
    this.ws = null;
  }

  getNotifications(): Observable<string> {
    return this.messageSubject.asObservable();
  }
}
