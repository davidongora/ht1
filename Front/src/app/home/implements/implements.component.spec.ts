import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImplementsComponent } from './implements.component';

describe('ImplementsComponent', () => {
  let component: ImplementsComponent;
  let fixture: ComponentFixture<ImplementsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ImplementsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ImplementsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
