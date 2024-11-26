import { Component, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
// import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  providers: [
    HttpClientModule
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
  
})
// export class AppComponent {
//   title = 'hello';
// }

// @Component({
//   selector: 'app-root',
//   standalone: true,
//   styleUrls: ['./app.component.css']
// })
export class AppComponent {
moveMap($event: Event) {
throw new Error('Method not implemented.');
}
move($event: Event) {
throw new Error('Method not implemented.');
}
  deferredPrompt: any;
center: any;
zoom: any;
display: any;

  constructor(@Inject(PLATFORM_ID) private platformId: Object) { }

  ngOnInit() {
    if (isPlatformBrowser(this.platformId)) {  // Ensure it's running in the browser
      window.addEventListener('beforeinstallprompt', (event) => {
        event.preventDefault();
        this.deferredPrompt = event;
        console.log('Install prompt saved to be triggered later.');
      });
    }
  }

  showInstallPrompt() {
    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      this.deferredPrompt.userChoice.then((choiceResult: any) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the install prompt');
        } else {
          console.log('User dismissed the install prompt');
        }
        this.deferredPrompt = null;
      });
    }
  }
}
