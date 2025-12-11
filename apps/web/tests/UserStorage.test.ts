import { validate } from '../src/service/AuthService';
import { getLocalStorageData, clearLocalStorageData, isUserLoggedIn, setLocalStorageData } from '../src/store/storage';

jest.mock('../src/service/AuthService', () => ({ validate: jest.fn() }));

describe('storage', () => {
  const key = 'khali_api6:user';
  const mockData = { id: 1, token: 'xyz789', permissions: [] };

  beforeEach(() => {
    localStorage.clear();
    jest.clearAllMocks();
  });

  it('getTokenFromLocalStorage returns object if present', () => {
    localStorage.setItem(key, JSON.stringify(mockData));
    expect(getLocalStorageData()).toMatchObject(mockData);
  });

  it('setLocalStorageData saves data correctly', () => {
    setLocalStorageData(mockData);
    // CORREÇÃO: Lemos a string e convertemos pra JSON antes de comparar
    const stored = JSON.parse(localStorage.getItem(key) || '{}');
    expect(stored).toMatchObject(mockData);
  });

  it('isUserLoggedIn returns true if token exists and validates', async () => {
    localStorage.setItem(key, JSON.stringify(mockData));
    (validate as jest.Mock).mockResolvedValue(true);
    expect(await isUserLoggedIn()).toBe(true);
  });
});
