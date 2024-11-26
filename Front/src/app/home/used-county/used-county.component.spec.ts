import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UsedCountyComponent } from './used-county.component';

describe('UsedCountyComponent', () => {
  let component: UsedCountyComponent;
  let fixture: ComponentFixture<UsedCountyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UsedCountyComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UsedCountyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
