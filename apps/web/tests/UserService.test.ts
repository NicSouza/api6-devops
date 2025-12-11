import { NewUser, User } from '../src/schemas/UserSchema';
import { Page } from '../src/schemas/pagination';
import {
  getUsers,
  getUser,
  createUser,
  updateUser,
  deleteUser,
} from '../src/service/UserService';
import {
  processGET,
  processPaginatedGET,
  processPOST,
  processRequest,
} from '../src/service/service';

jest.mock('../src/service/service');

jest.mock('../src/service/config', () => ({
  getApiBaseUrl: () => 'http://test-api',
  getAuthBaseUrl: () => 'http://test-auth',
  getPredictionBaseUrl: () => 'http://test-prediction',
}));

describe('UserService', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('getUsers', () => {
    it('should call processPaginatedGET with correct params and return result', async () => {
      const mockPage: Page<User> = {
        items: [], total: 0,
        totalPages: 0,
        size: 0
      };
      (processPaginatedGET as jest.Mock).mockResolvedValueOnce(mockPage);

      const result = await getUsers(1, 50);


      expect(processPaginatedGET).toHaveBeenCalledWith({
        path: `/users/`,
        page: 1,
        size: 50,
        overrideURL: 'http://test-auth'
      });
      expect(result).toBe(mockPage);
    });
  });

  describe('getUser', () => {
    it('should call processGET with correct params and return result', async () => {
      const mockUser: User = { id: '1', name: 'Test User' } as unknown as User;
      (processGET as jest.Mock).mockResolvedValueOnce(mockUser);

      const result = await getUser(1);

      expect(processGET).toHaveBeenCalledWith({
        path: `/user/1`,
        overrideURL: expect.anything(),
      });
      expect(result).toBe(mockUser);
    });
  });

  describe('createUser', () => {
    it('should call processPOST with correct params and return result', async () => {
      const newUser: NewUser = { name: 'New User', email: 'new@example.com' } as NewUser;
      const createdUser: User = { id: '2', ...newUser } as User;
      (processPOST as jest.Mock).mockResolvedValueOnce(createdUser);

      const result = await createUser(newUser);

      expect(processPOST).toHaveBeenCalledWith({
        path: `/register/`,
        body: newUser,
        overrideURL: 'http://test-auth',
      });
      expect(result).toBe(createdUser);
    });
  });

  describe('updateUser', () => {
    it('should call processRequest with correct params and return result', async () => {
      const updatedFields = { name: 'Updated Name' };
      const updatedUser: User = { id: '1', name: 'Updated Name' } as unknown as User;
      (processRequest as jest.Mock).mockResolvedValueOnce(updatedUser);

      const result = await updateUser(1, updatedFields);

      expect(processRequest).toHaveBeenCalledWith('PUT', {
        path: `/user/1`,
        body: updatedFields,
        overrideURL: expect.anything(),
      });
      expect(result).toBe(updatedUser);
    });
  });

  describe('deleteUser', () => {
    it('should call processRequest with DELETE and correct params', async () => {
      (processRequest as jest.Mock).mockResolvedValueOnce(undefined);

      await deleteUser(1);

      expect(processRequest).toHaveBeenCalledWith('DELETE', {
        path: `/user/1`,
        overrideURL: expect.anything(),
      });
    });
  });

});
