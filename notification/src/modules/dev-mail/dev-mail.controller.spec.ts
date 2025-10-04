import { Test, TestingModule } from '@nestjs/testing';
import { DevMailController } from './dev-mail.controller';

describe('DevMailController', () => {
  let controller: DevMailController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [DevMailController],
    }).compile();

    controller = module.get<DevMailController>(DevMailController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});
